import type { ChatItem, QuickReply } from "../../types/chat";
import { HospitalList } from "../hospitals/HospitalList";
import { ReportView } from "../handover/ReportView";
import { CitationList } from "./CitationList";
import { HospitalActions } from "./HospitalPopup";
import { QuickReplies } from "./QuickReplies";
import { StepCard } from "./StepCard";

type Props = { item: ChatItem; isLastWithActions: boolean; busy: boolean; onAction: (a: QuickReply["action"]) => void };

const venomColor = { yes: "border-emergency-500 bg-emergency-50", no: "border-success-500/40 bg-success-500/5", unknown: "border-amber-400 bg-amber-50" } as const;

/** Renders one chat item: user text, assistant text, step card, photo result, hospital prompt, hospitals or report. */
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
  if (m.type === "hospital_prompt") {
    return (
      <div className="max-w-xl rounded-2xl rounded-bl-md border border-emergency-500/30 bg-white px-4 py-3 text-sm shadow-soft">
        <p className="font-semibold text-ink-950">{m.text}</p>
        {m.hospital && <p className="mt-1 text-xs text-ink-500">Nearest: {m.hospital.name} ({m.hospital.distance_km} km)</p>}
        <HospitalActions prompt={m} />
      </div>
    );
  }
  if (m.type === "report") {
    return (
      <div className="w-full max-w-2xl space-y-3">
        <p className="rounded-2xl rounded-bl-md bg-white px-4 py-3 text-sm shadow-soft">{m.text}</p>
        <ReportView report={m.report} markdown={m.markdown} />
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