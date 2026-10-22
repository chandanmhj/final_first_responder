import type { MouseEvent } from "react";
import { api, getCoords } from "../../lib/api";
import type { ServerMessage } from "../../types/chat";

type Prompt = Extract<ServerMessage, { type: "hospital_prompt" }>;

/** The two choices: call 108, or open Google Maps directly to the hospital picked for this emergency. */
export function HospitalActions({ prompt, incidentId, onDone }: { prompt: Prompt; incidentId?: string | null; onDone?: () => void }) {
  const log = (type: string, text?: string) => { if (incidentId) void api.addEvent(incidentId, type, text).catch(() => undefined); };

  const navigate = async (e: MouseEvent) => {
    log("note", `Navigating to ${prompt.hospital?.name ?? "nearest hospital"}`);
    onDone?.();
    if (prompt.hospital) return; // hospital already chosen: the link opens Google Maps to it
    // No location was available earlier: get it now, pick the hospital for this emergency, then open Maps.
    e.preventDefault();
    const w = window.open("", "_blank");
    let url = prompt.maps_url;
    const c = await getCoords(8000);
    if (c) {
      try {
        const r = await api.hospitals(c.lat, c.lon, prompt.condition ?? undefined);
        if (r.results[0]) url = `${r.results[0].directions_url}&travelmode=driving`;
      } catch { /* keep fallback */ }
    }
    if (w) w.location.href = url; else window.location.href = url;
  };

  return (
    <div className="mt-4 grid gap-2">
      <a href="tel:108" onClick={() => { log("called_108"); onDone?.(); }} className="inline-flex h-12 items-center justify-center rounded-xl bg-emergency-600 text-sm font-bold text-white hover:bg-emergency-500">Call 108</a>
      <a href={prompt.maps_url} target="_blank" rel="noreferrer" onClick={(e) => void navigate(e)} className="inline-flex h-12 items-center justify-center rounded-xl border border-ink-200 bg-white text-sm font-semibold text-ink-900 hover:bg-ink-50">Navigate yourself</a>
    </div>
  );
}

export function HospitalPopup({ prompt, incidentId, onClose }: { prompt: Prompt; incidentId: string | null; onClose: () => void }) {
  return (
    <div role="dialog" aria-modal="true" className="fixed inset-0 z-50 grid place-items-center bg-ink-950/50 p-4">
      <div className="relative w-full max-w-sm rounded-3xl bg-white p-6 text-center shadow-soft">
        <button onClick={onClose} aria-label="Close" className="absolute right-3 top-3 grid size-9 place-items-center rounded-lg text-ink-500 hover:bg-ink-50">
          <svg viewBox="0 0 24 24" className="size-5" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" /></svg>
        </button>
        <h2 className="px-6 font-display text-xl font-bold text-ink-950">{prompt.text}</h2>
        {prompt.hospital && (
          <p className="mt-2 text-sm text-ink-500">
            Best match: {prompt.hospital.name} ({prompt.hospital.tier ? `${prompt.hospital.tier}, ` : ""}{prompt.hospital.distance_km} km)
          </p>
        )}
        <HospitalActions prompt={prompt} incidentId={incidentId} onDone={onClose} />
      </div>
    </div>
  );
}