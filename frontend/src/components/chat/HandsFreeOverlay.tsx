import type { HandsFreeState } from "../../hooks/useHandsFree";
import type { QuickReply } from "../../types/chat";

type Props = {
  state: HandsFreeState;
  level: number;
  transcript: string;
  stepText: string | null;
  error: string | null;
  onEnd: () => void;
  onAction: (a: QuickReply["action"]) => void;
};

const label: Record<HandsFreeState, string> = {
  off: "",
  listening: "Listening. Just talk.",
  hearing: "I hear you...",
  thinking: "Thinking...",
  speaking: "Speaking. You can talk over me.",
};

/** Full-screen, call-style voice mode. No record button: it listens and speaks by itself. */
export function HandsFreeOverlay({ state, level, transcript, stepText, error, onEnd, onAction }: Props) {
  if (state === "off") return null;
  const scale = 1 + (state === "hearing" ? level * 0.5 : state === "speaking" ? 0.18 : 0.04);
  const glow = state === "speaking" ? "bg-emergency-500" : state === "thinking" ? "bg-amber-400" : "bg-brand-500";
  return (
    <div className="fixed inset-0 z-50 flex flex-col items-center justify-between bg-ink-950 px-6 pb-[max(1.5rem,env(safe-area-inset-bottom))] pt-[max(1.5rem,env(safe-area-inset-top))] text-white" role="dialog" aria-label="Hands-free mode">
      <div className="w-full max-w-md text-center">
        <p className="text-xs font-semibold uppercase tracking-widest text-ink-300">Hands-free</p>
        {stepText && <p className="mt-4 font-display text-xl font-semibold leading-snug text-white/90">{stepText}</p>}
      </div>
      <div className="flex flex-col items-center gap-6">
        <div className="relative grid size-44 place-items-center">
          <div className={`absolute inset-0 rounded-full opacity-30 blur-2xl transition-transform duration-150 ${glow}`} style={{ transform: `scale(${scale * 1.2})` }} />
          <div className={`size-32 rounded-full shadow-lift transition-transform duration-150 ${glow} ${state === "thinking" ? "animate-pulse" : ""}`} style={{ transform: `scale(${scale})` }} />
        </div>
        <p className="text-lg font-semibold" role="status">{label[state]}</p>
        {transcript && <p className="max-w-sm text-center text-sm text-ink-300">"{transcript}"</p>}
        {error && <p className="max-w-sm rounded-xl bg-emergency-500/20 px-3 py-2 text-center text-sm text-emergency-50" role="alert">{error}</p>}
      </div>
      <div className="w-full max-w-md space-y-3">
        <div className="grid grid-cols-2 gap-3">
          <button onClick={() => onAction("next")} className="h-12 rounded-xl bg-white/10 text-sm font-semibold hover:bg-white/20">Done, next</button>
          <button onClick={() => onAction("not_worked")} className="h-12 rounded-xl bg-white/10 text-sm font-semibold hover:bg-white/20">Didn't work</button>
        </div>
        <button onClick={onEnd} className="h-12 w-full rounded-xl bg-emergency-500 text-sm font-bold hover:bg-emergency-600">End hands-free</button>
        <p className="text-center text-xs text-ink-300">Say "next", "it didn't work", "show hospitals" or "stop".</p>
      </div>
    </div>
  );
}
