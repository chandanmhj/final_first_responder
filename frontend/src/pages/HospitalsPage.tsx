import { useEffect, useState } from "react";
import { HospitalList } from "../components/hospitals/HospitalList";
import { Button } from "../components/ui/Button";
import { api, getCoords } from "../lib/api";
import type { Hospital } from "../types/chat";
import type { ConditionOption } from "../types/scenario";

/** Find suitable hospitals for an emergency type without starting a conversation. */
export default function HospitalsPage() {
  const [conds, setConds] = useState<ConditionOption[]>([]);
  const [cond, setCond] = useState("");
  const [res, setRes] = useState<Hospital[] | null>(null);
  const [msg, setMsg] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  useEffect(() => { api.conditions().then(setConds).catch(() => undefined); }, []);
  const find = async () => {
    setBusy(true); setMsg(null);
    const c = await getCoords();
    if (!c) { setMsg("Location is blocked. Allow location access, or call 108."); setBusy(false); return; }
    try { const r = await api.hospitals(c.lat, c.lon, cond || undefined); setRes(r.results); setMsg(r.message); } catch (e) { setMsg(e instanceof Error ? e.message : "Could not search."); }
    setBusy(false);
  };
  return (
    <div className="flex-1 overflow-y-auto px-4 py-8 sm:px-10"><div className="mx-auto max-w-2xl space-y-5">
      <h1 className="text-2xl font-bold text-ink-950">Find a hospital</h1>
      <select value={cond} onChange={(e) => setCond(e.target.value)} aria-label="Emergency type" className="h-11 w-full rounded-xl border border-ink-200 bg-white px-3 text-sm">
        <option value="">Any emergency</option>{conds.map((c) => <option key={c.id} value={c.id}>{c.title}</option>)}
      </select>
      <Button onClick={() => void find()} loading={busy}>Use my location</Button>
      {msg && <p className="rounded-xl bg-amber-50 px-4 py-3 text-sm text-amber-800">{msg}</p>}
      {res && <HospitalList hospitals={res} />}
    </div></div>
  );
}
