import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { ReportView } from "../components/handover/ReportView";
import { api } from "../lib/api";
import type { HandoverResponse } from "../types/handover";

export default function HandoverReportPage() {
  const { id = "" } = useParams();
  const [data, setData] = useState<HandoverResponse | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const load = useCallback(() => api.handover(id).then(setData).catch((e: unknown) => setErr(e instanceof Error ? e.message : "Could not load the report.")), [id]);
  useEffect(() => { void load(); }, [load]);
  return (
    <div className="flex-1 overflow-y-auto px-4 py-8 sm:px-10"><div className="mx-auto max-w-2xl">
      <h1 className="mb-5 text-2xl font-bold text-ink-950">Handover report</h1>
      {err && <p className="text-sm text-emergency-600">{err}</p>}
      {data && <ReportView report={data.report} markdown={data.markdown} onAddEvent={async (t, x) => { await api.addEvent(id, t, x); await load(); }} />}
    </div></div>
  );
}
