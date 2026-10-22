import { api } from "../../lib/api";
import type { ServerMessage } from "../../types/chat";

type Prompt = Extract<ServerMessage, { type: "hospital_prompt" }>;

/** The two choices: call 108, or open Google Maps to the nearest hospital. */
export function HospitalActions({ prompt, incidentId, onDone }: { prompt: Prompt; incidentId?: string | null; onDone?: () => void }) {
  const log = (type: string, text?: string) => { if (incidentId) void api.addEvent(incidentId, type, text).catch(() => undefined); };
  return (
    <div className="mt-4 grid gap-2">
      <a href="tel:108" onClick={() => { log("called_108"); onDone?.(); }} className="inline-flex h-12 items-center justify-center rounded-xl bg-emergency-600 text-sm font-bold text-white hover:bg-emergency-500">Call 108</a>
      <a href={prompt.maps_url} target="_blank" rel="noreferrer" onClick={() => { log("note", `Navigating to ${prompt.hospital?.name ?? "nearest hospital"}`); onDone?.(); }} className="inline-flex h-12 items-center justify-center rounded-xl border border-ink-200 bg-white text-sm font-semibold text-ink-900 hover:bg-ink-50">Navigate yourself</a>
    </div>
  );
}

export function HospitalPopup({ prompt, incidentId, onClose }: { prompt: Prompt; incidentId: string | null; onClose: () => void }) {
  return (
    <div role="dialog" aria-modal="true" className="fixed inset-0 z-50 grid place-items-center bg-ink-950/50 p-4">
      <div className="w-full max-w-sm rounded-3xl bg-white p-6 text-center shadow-soft">
        <h2 className="font-display text-xl font-bold text-ink-950">{prompt.text}</h2>
        {prompt.hospital && <p className="mt-2 text-sm text-ink-500">Nearest suitable hospital: {prompt.hospital.name} ({prompt.hospital.distance_km} km)</p>}
        <HospitalActions prompt={prompt} incidentId={incidentId} onDone={onClose} />
      </div>
    </div>
  );
}