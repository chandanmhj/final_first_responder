import { useMediaPrefetch } from "../../hooks/useMediaPrefetch";
import type { QuickReply, StepData } from "../../types/chat";
import { MediaPlayer } from "./MediaPlayer";
import { QuickReplies } from "./QuickReplies";

type Props = { step: StepData; replies: QuickReply[]; active: boolean; onPick: (a: QuickReply["action"]) => void; busy: boolean };

/** One instruction: big readable text, optional media, and fast reply buttons while it is the current step. */
export function StepCard({ step, replies, active, onPick, busy }: Props) {
  useMediaPrefetch(active ? step.next_media : null);
  const pct = Math.round(((step.index + 1) / step.total) * 100);
  return (
    <article className={`w-full max-w-xl rounded-2xl border bg-white p-5 shadow-soft ${active ? "border-brand-100 ring-4 ring-brand-50" : "border-ink-100 opacity-90"}`}>
      <header className="mb-3 flex items-center justify-between gap-3">
        <span className="rounded-full bg-brand-50 px-3 py-1 text-xs font-bold text-brand-700">
          Step {step.index + 1} of {step.total}
        </span>
        <div className="h-1.5 w-24 overflow-hidden rounded-full bg-ink-100" aria-hidden="true">
          <div className="h-full rounded-full bg-brand-500 transition-all" style={{ width: `${pct}%` }} />
        </div>
      </header>
      <p className="font-display text-xl font-semibold leading-snug text-ink-950">{step.text}</p>
      <MediaPlayer media={step.media} title={step.text} />
      {step.unreviewed_note && <p className="mt-3 rounded-lg bg-amber-50 px-3 py-2 text-xs text-amber-800">{step.unreviewed_note}</p>}
      <p className="mt-3 text-[11px] leading-snug text-ink-500">Source: {step.source_label}</p>
      {active && <QuickReplies replies={replies} onPick={onPick} disabled={busy} />}
    </article>
  );
}
