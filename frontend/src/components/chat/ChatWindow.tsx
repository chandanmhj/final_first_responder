import { useEffect, useRef } from "react";
import type { ChatItem, QuickReply } from "../../types/chat";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";

type Props = { items: ChatItem[]; sending: boolean; error: string | null; onAction: (a: QuickReply["action"]) => void };

function hasActions(item: ChatItem): boolean {
  const m = item.message;
  return (m.type === "step") || (m.type === "text" && !!m.quick_replies?.length);
}

/** The scrolling message list. Only the newest card with buttons keeps its buttons active. */
export function ChatWindow({ items, sending, error, onAction }: Props) {
  const end = useRef<HTMLDivElement>(null);
  useEffect(() => {
    end.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [items.length, sending]);
  let lastIdx = -1;
  items.forEach((it, i) => {
    if (it.from === "assistant" && hasActions(it)) lastIdx = i;
  });
  return (
    <div className="flex-1 space-y-4 overflow-y-auto px-4 py-6 sm:px-8" aria-live="polite">
      {items.map((it, i) => (
        <MessageBubble key={it.id} item={it} isLastWithActions={i === lastIdx} busy={sending} onAction={onAction} />
      ))}
      {sending && <TypingIndicator />}
      {error && <p className="max-w-xl rounded-xl bg-emergency-50 px-4 py-3 text-sm text-emergency-600" role="alert">{error}</p>}
      <div ref={end} />
    </div>
  );
}
