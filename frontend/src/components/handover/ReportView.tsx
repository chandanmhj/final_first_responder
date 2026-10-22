import { useState } from "react";
import type { HandoverReport } from "../../types/chat";
import { Button } from "../ui/Button";

const ACTIONS: [string, string][] = [
  ["called_108", "Called 108"],
  ["ambulance_arrived", "Ambulance arrived"],
  ["cpr_started", "CPR started"],
  ["aed_used", "AED used"],
  ["tourniquet_applied", "Tourniquet applied"],
  ["patient_moved", "Patient moved"],
];

const LABELS: [string, string][] = [["age", "Age"], ["sex", "Sex"], ["blood_group", "Blood group"], ["allergies", "Allergies"], ["conditions", "Medical conditions"], ["medications", "Medicines"], ["emergency_contact", "Emergency contact"]];

type Props = { report: HandoverReport; markdown: string; onAddEvent?: (type: string, text?: string) => Promise<void> };

const fmt = (iso: string) => new Date(iso).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });

/** The ISBAR handover report with a timestamped timeline, copy/print, and (on the report page) quick event buttons. */
export function ReportView({ report, markdown, onAddEvent }: Props) {
  const [note, setNote] = useState("");
  const [copied, setCopied] = useState(false);
  const [busy, setBusy] = useState(false);
  const add = async (type: string, text?: string) => {
    if (!onAddEvent) return;
    setBusy(true);
    try {
      await onAddEvent(type, text);
    } finally {
      setBusy(false);
    }
  };
  const d = report.identify.patient_details;
  const Section = ({ letter, title, children }: { letter: string; title: string; children: React.ReactNode }) => (
    <section className="rounded-2xl border border-ink-100 bg-white p-5 shadow-soft print:shadow-none">
      <h2 className="flex items-center gap-3 font-display text-lg font-bold text-ink-950">
        <span className="grid size-8 place-items-center rounded-lg bg-brand-600 text-sm text-white">{letter}</span>
        {title}
      </h2>
      <div className="mt-3 text-sm text-ink-700">{children}</div>
    </section>
  );
  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2 print:hidden">
        <Button variant="secondary" onClick={() => void navigator.clipboard.writeText(markdown).then(() => { setCopied(true); setTimeout(() => setCopied(false), 1500); })}>
          {copied ? "Copied" : "Copy as text"}
        </Button>
        <Button variant="secondary" onClick={() => window.print()}>Print</Button>
      </div>
      <Section letter="I" title="Identify">
        <ul className="space-y-1">
          <li>Reported by: {report.identify.reported_by_role === "responder" ? "Certified first responder" : "Common person"}</li>
          <li>Patient: {report.identify.patient}, age group {report.identify.age_band ?? "unknown"}</li>
          <li>Started: {report.identify.started_at ? new Date(report.identify.started_at).toLocaleString() : "unknown"}</li>
          {LABELS.map(([k, l]) => (d?.[k] ? <li key={k}>{l}: {d[k]}</li> : null))}
        </ul>
      </Section>
      <Section letter="S" title="Situation">{report.situation.what_happened}</Section>
      <Section letter="B" title="Background">
        {report.background.notes.length ? <ul className="list-disc space-y-1 pl-5">{report.background.notes.map((n, i) => <li key={i}>{n}</li>)}</ul> : "Nothing recorded yet."}
      </Section>
      <Section letter="A" title="Assessment and actions">
        <ol className="space-y-2">
          {report.assessment_and_actions.map((t, i) => (
            <li key={i} className="flex gap-3">
              <time className="w-20 shrink-0 font-mono text-xs text-ink-500">{fmt(t.time)}</time>
              <span>{t.text}</span>
            </li>
          ))}
        </ol>
      </Section>
      <Section letter="R" title="Recommendation">
        <p>Hospital needs: {report.recommendation.facility_needs ?? "nearest emergency department"}</p>
        <p>Ambulance: {report.recommendation.call}</p>
      </Section>
      {onAddEvent && (
        <section className="rounded-2xl border border-ink-100 bg-white p-5 shadow-soft print:hidden">
          <h2 className="font-display text-base font-bold text-ink-950">Add to the timeline</h2>
          <div className="mt-3 flex flex-wrap gap-2">
            {ACTIONS.map(([type, label]) => (
              <button key={type} disabled={busy} onClick={() => void add(type)} className="rounded-full border border-ink-200 bg-white px-3.5 py-1.5 text-xs font-semibold hover:bg-ink-50 disabled:opacity-50">
                {label}
              </button>
            ))}
          </div>
          <div className="mt-3 flex gap-2">
            <input value={note} onChange={(e) => setNote(e.target.value)} placeholder="Add a note (allergies, medicines, what you saw)" className="h-11 flex-1 rounded-xl border border-ink-200 px-3.5 text-sm focus:border-brand-500 focus:outline-none focus:ring-4 focus:ring-brand-100" />
            <Button disabled={!note.trim() || busy} onClick={() => void add("note", note.trim()).then(() => setNote(""))}>Add</Button>
          </div>
        </section>
      )}
    </div>
  );
}