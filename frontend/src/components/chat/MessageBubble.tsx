import { Link } from "react-router-dom";
import type { ChatItem, QuickReply } from "../../types/chat";
import { HospitalList } from "../hospitals/HospitalList";
import { CitationList } from "./CitationList";
import { QuickReplies } from "./QuickReplies";
import { StepCard } from "./StepCard";

type Props = { item: ChatItem; isLastWithActions: boolean; busy: boolean; onAction: (a: QuickReply["action"]) => void };

const venomColor = { yes: "border-emergency-500 bg-emergency-50", no: "border-success-500/40 bg-success-500/5", unknown: "border-amber-400 bg-amber-50" } as const;

/** Renders one chat item: user text, assistant text, step card, photo result, hospitals or report link. */
export function MessageBubble({ item, isLastWithActions, busy, onAction }: Props) {
  const m = item.message;
  if (m.type === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-[85%] rounded-2xl rounded-br-md bg-brand-600 px-4 py-3 text-sm text-white shadow-soft">
          {m.imageUrl && <img src={m.imageUrl} alt="Your photo" className="mb-2 max-h-56 rounded-xl" />}
          {m.hasImage && !m.imageUrl && <p className="mb-1 text-xs opacity-80">Photo sent</p>}
          {m.text && <p className="whitespace-pre-wrap">{m.text}</p>}
        </div>
      </div>
    );
  }
  if (m.type === "step") return <StepCard step={m.step} replies={m.quick_replies} active={isLastWithActions} onPick={onAction} busy={busy} />;
  if (m.type === "animal") {
    return (
      <div className={`max-w-xl rounded-2xl border-2 p-4 shadow-soft ${venomColor[m.result.venomous]}`}>
        <p className="font-display text-lg font-bold text-ink-950">{m.result.headline}</p>
        <ul className="mt-2 space-y-1 text-sm text-ink-700">{m.result.advice.map((a) => <li key={a}>• {a}</li>)}</ul>
        <p className="mt-3 text-[11px] text-ink-500">A photo cannot confirm what an animal is. This is a best guess to help you act quickly, not a diagnosis.</p>
      </div>
    );
  }
  if (m.type === "hospitals") {
    return (
      <div className="space-y-2">
        <p className="max-w-xl rounded-2xl rounded-bl-md bg-white px-4 py-3 text-sm shadow-soft">{m.text}</p>
        <HospitalList hospitals={m.hospitals} need={m.need} />
      </div>
    );
  }
  if (m.type === "report") {
    return (
      <div className="max-w-xl rounded-2xl rounded-bl-md bg-white px-4 py-3 text-sm shadow-soft">
        <p>{m.text}</p>
        <Link to={`/app/incident/${m.incident_id}/report`} className="mt-3 inline-flex h-10 items-center rounded-xl bg-brand-600 px-4 text-sm font-semibold text-white hover:bg-brand-700">
          Open handover report
        </Link>
      </div>
    );
  }
  const crisis = m.type === "text" && m.crisis;
  return (
    <div className={`max-w-xl rounded-2xl rounded-bl-md px-4 py-3 text-sm shadow-soft ${crisis ? "border border-brand-100 bg-brand-50" : "bg-white"}`}>
      <p className="whitespace-pre-wrap leading-relaxed text-ink-900">{m.text}</p>
      {m.type === "text" && <CitationList citations={m.citations} />}
      {m.type === "text" && m.quick_replies && isLastWithActions && <QuickReplies replies={m.quick_replies} onPick={onAction} disabled={busy} />}
    </div>
  );
}
