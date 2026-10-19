import { useCallback, useRef, useState } from "react";
import { api, ApiError } from "../lib/api";
import type { QuickReply } from "../types/chat";
import { useAudioPlayback } from "./useAudioPlayback";
import { useVoiceActivity } from "./useVoiceActivity";

export type HandsFreeState = "off" | "listening" | "hearing" | "thinking" | "speaking";

type Props = {
  /** Send recognised text to the chat. Returns the text to read aloud. */
  onText: (text: string) => Promise<string | null>;
  /** Run a quick-reply action by voice (next, not worked, hospitals...). Returns the text to read aloud. */
  onAction: (action: QuickReply["action"]) => Promise<string | null>;
};

/** Spoken commands that map to quick-reply buttons. Anything else goes to the chat as a normal message. */
export function matchCommand(t: string): QuickReply["action"] | "repeat" | "end" | null {
  const s = t.toLowerCase().replace(/[.,!?]/g, "").trim();
  if (/^(next|next step|done|okay next|ok next|continue|go on|i did it|finished|yes done)$/.test(s)) return "next";
  if (/(did ?n'?o?t work|not working|doesn'?t work|no change|still (bleeding|choking))/.test(s)) return "not_worked";
  if (/(show|find|nearest|nearby).*(hospital)/.test(s)) return "hospitals";
  if (/(handover|report)/.test(s)) return "report";
  if (/^(repeat|say that again|say again|what)$/.test(s)) return "repeat";
  if (/(stop|end|exit|turn off).*(hands.?free|call|listening|voice)/.test(s) || s === "stop") return "end";
  return null;
}

/** Call-style voice mode: listens and speaks, and sends speech to the chat by itself when the user pauses. */
export function useHandsFree({ onText, onAction }: Props) {
  const [active, setActive] = useState(false);
  const [thinking, setThinking] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [error, setError] = useState<string | null>(null);
  const speech = useAudioPlayback();
  const lastSpoken = useRef("");
  const busy = useRef(false);

  const say = useCallback(
    async (text: string | null) => {
      if (!text) return;
      lastSpoken.current = text;
      await speech.speak(text);
    },
    [speech],
  );

  const handleWav = useCallback(
    async (wav: Blob) => {
      if (busy.current) return;
      busy.current = true;
      setThinking(true);
      try {
        const { text } = await api.transcribe(wav);
        if (!text) return;
        setTranscript(text);
        const cmd = matchCommand(text);
        if (cmd === "end") {
          setActive(false);
          return;
        }
        if (cmd === "repeat") return void (await say(lastSpoken.current));
        const reply = cmd ? await onAction(cmd) : await onText(text);
        await say(reply);
      } catch (e) {
        setError(e instanceof ApiError ? e.message : "I couldn't hear that. Please try again.");
      } finally {
        busy.current = false;
        setThinking(false);
      }
    },
    [onAction, onText, say],
  );

  const vad = useVoiceActivity({
    isSpeaking: () => speech.speakingRef.current,
    onSpeechStart: () => speech.cancel(),
    onUtterance: (wav) => void handleWav(wav),
  });

  const start = useCallback(async () => {
    setError(null);
    setActive(true);
    await vad.start();
  }, [vad]);

  const stop = useCallback(() => {
    vad.stop();
    speech.cancel();
    setActive(false);
    setThinking(false);
  }, [vad, speech]);

  const state: HandsFreeState = !active ? "off" : speech.speaking ? "speaking" : thinking ? "thinking" : vad.hearing ? "hearing" : "listening";
  return { active, state, level: vad.level, transcript, error: error ?? vad.error, start, stop, say, supported: speech.supported && !!navigator.mediaDevices };
}
