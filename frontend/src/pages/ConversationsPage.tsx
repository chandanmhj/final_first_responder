import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "../components/ui/Button";
import { useProfile } from "../hooks/useProfile";
import { api } from "../lib/api";
import type { SessionSummary } from "../types/chat";

const QUICK = ["Chest pain", "Someone is choking", "Heavy bleeding", "Snake bite", "Not breathing", "Road accident", "Burn", "Seizure"];

/** Home: welcome card with a box to start, quick-start chips, and the list of past conversations. */
export default function ConversationsPage() {
  const navigate = useNavigate();
  const { profile } = useProfile();
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [q, setQ] = useState("");
  const [text, setText] = useState("");
  const [asc, setAsc] = useState(false);

  useEffect(() => { api.listSessions().then(setSessions).catch(() => undefined); }, []);
  const shown = useMemo(() => {
    const l = sessions.filter((s) => s.title.toLowerCase().includes(q.toLowerCase()));
    return asc ? [...l].reverse() : l;
  }, [sessions, q, asc]);
  const go = (t: string) => navigate("/app/c/new", { state: { start: t } });
  const name = (profile?.full_name ?? "").split(" ")[0] || "there";

  return (
    <div className="flex-1 overflow-y-auto px-4 py-8 sm:px-10">
      <div className="mx-auto max-w-3xl">
        <section className="rounded-3xl border border-ink-100 bg-white p-8 text-center shadow-soft">
          <h1 className="text-3xl font-bold text-ink-950">Welcome back, {name}</h1>
          <p className="mt-1 text-sm text-ink-500">Tell me what is happening. If someone is in danger, call 108 first.</p>
          <form className="mx-auto mt-6 flex max-w-xl gap-2" onSubmit={(e) => { e.preventDefault(); if (text.trim()) go(text.trim()); }}>
            <input value={text} onChange={(e) => setText(e.target.value)} placeholder="How can I assist you today?" aria-label="Describe the emergency" className="h-12 flex-1 rounded-xl border border-ink-200 px-4 text-sm focus:border-brand-500 focus:outline-none focus:ring-4 focus:ring-brand-100" />
            <Button type="submit" className="h-12">Start</Button>
          </form>
          <div className="mt-5 flex flex-wrap justify-center gap-2">{QUICK.map((c) => <button key={c} onClick={() => go(c)} className="rounded-full border border-ink-200 bg-white px-3.5 py-1.5 text-xs font-semibold text-ink-700 hover:bg-ink-50">{c}</button>)}</div>
        </section>
        <div className="mt-10 flex flex-wrap items-center justify-between gap-3">
          <h2 className="font-display text-lg font-bold text-ink-950">Conversations ({sessions.length})</h2>
          <div className="flex gap-2">
            <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search conversations..." aria-label="Search" className="h-10 rounded-xl border border-ink-200 px-3 text-sm focus:border-brand-500 focus:outline-none" />
            <button onClick={() => setAsc(!asc)} className="h-10 rounded-xl border border-ink-200 bg-white px-3 text-sm text-ink-700">{asc ? "Oldest first" : "Newest first"}</button>
          </div>
        </div>
        <ul className="mt-4 space-y-2">
          {shown.map((s) => (
            <li key={s.id}>
              <Link to={`/app/c/${s.id}`} className="flex items-center justify-between gap-3 rounded-xl border border-ink-100 bg-white px-4 py-3 shadow-soft hover:border-brand-100">
                <span className="truncate text-sm font-medium text-ink-900">{s.title}</span>
                <span className="flex shrink-0 items-center gap-3 text-xs text-ink-500">
                  {s.status === "active" && <span className="rounded-full bg-emergency-50 px-2 py-0.5 font-semibold text-emergency-600">In progress</span>}
                  {new Date(s.updated_at).toLocaleDateString()}
                </span>
              </Link>
            </li>
          ))}
          {!shown.length && <li className="rounded-xl border border-dashed border-ink-200 p-8 text-center text-sm text-ink-500">No conversations yet.</li>}
        </ul>
      </div>
    </div>
  );
}
