import { useCallback, useEffect, useRef, useState } from "react";

/** Prefer natural-sounding English voices. Browser voices differ by device, so we score what is available. */
function pickVoice(voices: SpeechSynthesisVoice[]): SpeechSynthesisVoice | null {
  const en = voices.filter((v) => v.lang.toLowerCase().startsWith("en"));
  const score = (v: SpeechSynthesisVoice) => {
    let s = 0;
    if (/natural|neural|online/i.test(v.name)) s += 6;
    if (/google/i.test(v.name)) s += 4;
    if (/samantha|aria|jenny|sonia|libby|ryan|daniel|karen|moira|veena|rishi|heera/i.test(v.name)) s += 3;
    if (/en-in/i.test(v.lang)) s += 2;
    if (/en-gb|en-us/i.test(v.lang)) s += 1;
    if (v.localService) s -= 1;
    return s;
  };
  return [...en].sort((a, b) => score(b) - score(a))[0] ?? null;
}

function sentences(text: string): string[] {
  return text.match(/[^.!?]+[.!?]*/g)?.map((s) => s.trim()).filter(Boolean) ?? [text];
}

/** Text to speech with the browser voice (decision 0015): short sentences, slightly quicker rate, best available voice. */
export function useAudioPlayback() {
  const [speaking, setSpeaking] = useState(false);
  const speakingRef = useRef(false);
  const voiceRef = useRef<SpeechSynthesisVoice | null>(null);
  const supported = typeof window !== "undefined" && "speechSynthesis" in window;

  useEffect(() => {
    if (!supported) return;
    const load = () => {
      voiceRef.current = pickVoice(window.speechSynthesis.getVoices());
    };
    load();
    window.speechSynthesis.addEventListener("voiceschanged", load);
    return () => window.speechSynthesis.removeEventListener("voiceschanged", load);
  }, [supported]);

  const cancel = useCallback(() => {
    if (!supported) return;
    window.speechSynthesis.cancel();
    speakingRef.current = false;
    setSpeaking(false);
  }, [supported]);

  const speak = useCallback(
    (text: string): Promise<void> =>
      new Promise((resolve) => {
        if (!supported || !text) return resolve();
        window.speechSynthesis.cancel();
        const parts = sentences(text);
        speakingRef.current = true;
        setSpeaking(true);
        parts.forEach((part, i) => {
          const u = new SpeechSynthesisUtterance(part);
          if (voiceRef.current) u.voice = voiceRef.current;
          u.lang = voiceRef.current?.lang ?? "en-IN";
          u.rate = 1.05;
          u.pitch = 1;
          const last = i === parts.length - 1;
          u.onend = () => {
            if (last) {
              speakingRef.current = false;
              setSpeaking(false);
              resolve();
            }
          };
          u.onerror = () => {
            if (last) {
              speakingRef.current = false;
              setSpeaking(false);
              resolve();
            }
          };
          window.speechSynthesis.speak(u);
        });
      }),
    [supported],
  );

  return { speak, cancel, speaking, speakingRef, supported };
}
