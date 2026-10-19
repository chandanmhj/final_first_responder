import type { QuickReply } from "../../types/chat";

type Props = { replies: QuickReply[]; onPick: (a: QuickReply["action"]) => void; disabled?: boolean };

const tone: Record<string, string> = {
  next: "bg-brand-600 text-white hover:bg-brand-700 shadow-soft",
  not_worked: "border border-emergency-500/40 bg-emergency-50 text-emergency-600 hover:bg-emergency-50/70",
};

/** Fast answers under a step: Next and a step-specific "did not work" button. */
export function QuickReplies({ replies, onPick, disabled }: Props) {
  return (
    <div className="mt-4 flex flex-wrap gap-2">
      {replies.map((r) => (
        <button
          key={r.id}
          type="button"
          disabled={disabled}
          onClick={() => onPick(r.action)}
          className={`h-11 rounded-xl px-5 text-sm font-semibold transition-colors disabled:opacity-50 ${tone[r.action] ?? "border border-ink-200 bg-white text-ink-900 hover:bg-ink-50"}`}
        >
          {r.label}
        </button>
      ))}
    </div>
  );
}
