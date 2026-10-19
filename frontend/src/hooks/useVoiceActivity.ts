import { useCallback, useEffect, useRef, useState } from "react";
import { encodeWav, rms } from "../lib/audio";

type Options = {
  /** True while the assistant is speaking: the detector becomes less sensitive so it does not hear itself. */
  isSpeaking: () => boolean;
  /** Called when the user starts talking (use it to stop the assistant: barge-in). */
  onSpeechStart: () => void;
  /** Called with one finished utterance as a 16 kHz WAV. */
  onUtterance: (wav: Blob) => void;
};

const FRAME = 4096;
const SILENCE_END_S = 1.0; // pause that ends a turn
const MIN_SPEECH_S = 0.4;
const MAX_UTTERANCE_S = 20;

/**
 * Energy-based voice activity detection on the microphone. Listens all the time and decides by itself when the user has
 * finished speaking. Echo cancellation is requested from the browser, and sensitivity drops while the assistant talks.
 * Works on phones without extra model files. Tune the constants above on real devices.
 */
export function useVoiceActivity({ isSpeaking, onSpeechStart, onUtterance }: Options) {
  const [listening, setListening] = useState(false);
  const [hearing, setHearing] = useState(false);
  const [level, setLevel] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const cleanup = useRef<(() => void) | null>(null);
  const cb = useRef({ isSpeaking, onSpeechStart, onUtterance });

  useEffect(() => {
    cb.current = { isSpeaking, onSpeechStart, onUtterance };
  });

  const stop = useCallback(() => {
    cleanup.current?.();
    cleanup.current = null;
    setListening(false);
    setHearing(false);
    setLevel(0);
  }, []);

  const start = useCallback(async () => {
    if (cleanup.current) return;
    setError(null);
    let stream: MediaStream;
    try {
      stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true } });
    } catch {
      setError("Microphone access was blocked. Allow the microphone to use hands-free mode.");
      return;
    }
    const ctx = new AudioContext();
    const source = ctx.createMediaStreamSource(stream);
    const proc = ctx.createScriptProcessor(FRAME, 1, 1);
    const mute = ctx.createGain();
    mute.gain.value = 0;
    source.connect(proc);
    proc.connect(mute);
    mute.connect(ctx.destination);

    const frameSec = FRAME / ctx.sampleRate;
    let floor = 0.01;
    let inSpeech = false;
    let loud = 0;
    let silent = 0;
    let utter: Float32Array[] = [];
    const preroll: Float32Array[] = [];

    proc.onaudioprocess = (e) => {
      const data = new Float32Array(e.inputBuffer.getChannelData(0));
      const level = rms(data);
      const talking = cb.current.isSpeaking();
      if (!inSpeech) floor = floor * 0.95 + level * 0.05;
      const threshold = Math.max(0.015, floor * 3) * (talking ? 2.4 : 1);
      setLevel(Math.min(1, level * 8));
      const isLoud = level > threshold;
      if (!inSpeech) {
        preroll.push(data);
        if (preroll.length > 3) preroll.shift();
        loud = isLoud ? loud + 1 : 0;
        if (loud >= (talking ? 4 : 2)) {
          inSpeech = true;
          silent = 0;
          utter = [...preroll];
          setHearing(true);
          cb.current.onSpeechStart();
        }
        return;
      }
      utter.push(data);
      silent = isLoud ? 0 : silent + 1;
      const dur = utter.length * frameSec;
      if ((silent * frameSec >= SILENCE_END_S && dur >= MIN_SPEECH_S + SILENCE_END_S) || dur >= MAX_UTTERANCE_S) {
        const wav = encodeWav(utter, ctx.sampleRate);
        inSpeech = false;
        loud = 0;
        utter = [];
        preroll.length = 0;
        setHearing(false);
        cb.current.onUtterance(wav);
      } else if (silent * frameSec >= SILENCE_END_S && dur < MIN_SPEECH_S + SILENCE_END_S) {
        inSpeech = false; // too short: a click or cough
        loud = 0;
        utter = [];
        setHearing(false);
      }
    };

    cleanup.current = () => {
      proc.disconnect();
      source.disconnect();
      mute.disconnect();
      stream.getTracks().forEach((t) => t.stop());
      void ctx.close();
    };
    setListening(true);
  }, []);

  useEffect(() => () => cleanup.current?.(), []);

  return { listening, hearing, level, error, start, stop };
}
