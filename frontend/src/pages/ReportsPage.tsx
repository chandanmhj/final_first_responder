import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../lib/api";
import type { IncidentSummary } from "../types/handover";

export default function ReportsPage() {
  const [items, setItems] = useState<IncidentSummary[]>([]);
  useEffect(() => { api.incidents().then(setItems).catch(() => undefined); }, []);
  return (
    <div className="flex-1 overflow-y-auto px-4 py-8 sm:px-10"><div className="mx-auto max-w-2xl">
      <h1 className="text-2xl font-bold text-ink-950">Handover reports</h1>
      <ul className="mt-5 space-y-2">
        {items.map((i) => <li key={i.id}><Link to={`/app/incident/${i.id}/report`} className="flex justify-between rounded-xl border border-ink-100 bg-white px-4 py-3 text-sm shadow-soft hover:border-brand-100"><span className="font-medium">{i.title}</span><span className="text-ink-500">{new Date(i.started_at).toLocaleString()}</span></Link></li>)}
        {!items.length && <li className="rounded-xl border border-dashed border-ink-200 p-8 text-center text-sm text-ink-500">No reports yet. One is created for every emergency.</li>}
      </ul>
    </div></div>
  );
}
