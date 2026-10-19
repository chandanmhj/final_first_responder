import type { Hospital } from "../../types/chat";

const tierLabel: Record<string, string> = { tertiary: "Major hospital", secondary: "Hospital", primary: "Clinic or health centre" };

/** Ranked hospitals with distance, why they were chosen, and one-tap directions and call. */
export function HospitalList({ hospitals, need }: { hospitals: Hospital[]; need?: string | null }) {
  if (!hospitals.length) return null;
  return (
    <div className="w-full max-w-xl space-y-3">
      {need && <p className="rounded-xl bg-brand-50 px-3.5 py-2.5 text-sm text-brand-700">Best place for this emergency: {need}</p>}
      {hospitals.map((h, i) => (
        <article key={h.id} className={`rounded-2xl border bg-white p-4 shadow-soft ${i === 0 ? "border-brand-100 ring-4 ring-brand-50" : "border-ink-100"}`}>
          <div className="flex items-start justify-between gap-3">
            <div>
              {i === 0 && <span className="mb-1 inline-block rounded-full bg-success-500/10 px-2 py-0.5 text-[11px] font-bold text-success-500">Best match</span>}
              <h3 className="font-display text-base font-bold text-ink-950">{h.name}</h3>
              <p className="text-xs text-ink-500">{tierLabel[h.tier] ?? h.tier} · {h.distance_km} km away</p>
            </div>
          </div>
          <ul className="mt-2 flex flex-wrap gap-1.5">
            {h.reasons.map((r) => (
              <li key={r} className="rounded-full bg-ink-50 px-2.5 py-1 text-[11px] text-ink-700">{r}</li>
            ))}
          </ul>
          <div className="mt-3 flex gap-2">
            <a href={h.directions_url} target="_blank" rel="noreferrer" className="inline-flex h-10 flex-1 items-center justify-center rounded-xl bg-brand-600 text-sm font-semibold text-white hover:bg-brand-700">
              Directions
            </a>
            {h.call_url && (
              <a href={h.call_url} className="inline-flex h-10 flex-1 items-center justify-center rounded-xl border border-ink-200 bg-white text-sm font-semibold text-ink-900 hover:bg-ink-50">
                Call
              </a>
            )}
          </div>
        </article>
      ))}
      <p className="text-[11px] text-ink-500">Capabilities marked "inferred" are guessed from the name. Confirm by phone if you can. In an emergency, call 108.</p>
    </div>
  );
}
