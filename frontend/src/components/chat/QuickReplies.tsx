import type { QuickReply } from "../../types/chat";

type Props = { replies: QuickReply[]; onPick: (a: QuickReply["action"], text?: string) => void; disabled?: boolean };

const tone: Record<string, string> = {
  next: "h-11 px-5 font-semibold bg-brand-600 text-white hover:bg-brand-700 shadow-soft",
  not_worked: "h-11 px-5 font-semibold border border-emergency-500/40 bg-emergency-50 text-emergency-600 hover:bg-emergency-50/70",
  ask: "min-h-10 px-4 py-2 font-medium border border-brand-100 bg-brand-50 text-brand-700 hover:bg-brand-100 text-left",
};

/** Buttons under a reply: answers to the question just asked, then Next and "didn't work". */
export function QuickReplies({ replies, onPick, disabled }: Props) {
  return (
    <div className="mt-4 flex flex-wrap gap-2">
      {replies.map((r) => (
        <button
          key={r.id}
          type="button"
          disabled={disabled}
          onClick={() => onPick(r.action, r.text ?? r.label)}
          className={`rounded-xl text-sm transition-colors disabled:opacity-50 ${tone[r.action] ?? "h-11 px-5 font-semibold border border-ink-200 bg-white text-ink-900 hover:bg-ink-50"}`}
        >
          {r.label}
        </button>
      ))}
    </div>
  );
}