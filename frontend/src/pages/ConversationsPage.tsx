import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../lib/api";
import type { SessionSummary } from "../types/chat";

const item = "block w-full rounded-lg px-3 py-2 text-left text-sm hover:bg-ink-50 disabled:text-ink-300 disabled:hover:bg-transparent";

/** Previous conversations only, each with a three-dots menu: pin, delete, show handover report. */
export default function ConversationsPage() {
  const navigate = useNavigate();
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [q, setQ] = useState("");
  const [asc, setAsc] = useState(false);
  const [menu, setMenu] = useState<string | null>(null);

  useEffect(() => { api.listSessions().then(setSessions).catch(() => undefined); }, []);
  const shown = useMemo(() => {
    const l = sessions.filter((s) => s.title.toLowerCase().includes(q.toLowerCase()));
    return [...(asc ? [...l].reverse() : l)].sort((a, b) => Number(!!b.pinned) - Number(!!a.pinned));
  }, [sessions, q, asc]);

  const togglePin = async (s: SessionSummary) => {
    setMenu(null);
    try { await api.pinSession(s.id, !s.pinned); setSessions((p) => p.map((x) => (x.id === s.id ? { ...x, pinned: !s.pinned } : x))); } catch { /* ignore */ }
  };
  const remove = async (s: SessionSummary) => {
    setMenu(null);
    if (!window.confirm("Delete this chat?")) return;
    try { await api.deleteSession(s.id); setSessions((p) => p.filter((x) => x.id !== s.id)); } catch { /* ignore */ }
  };

  return (
    <div className="flex-1 overflow-y-auto px-4 py-8 sm:px-10">
      <div className="mx-auto max-w-3xl">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h1 className="font-display text-2xl font-bold text-ink-950">Previous conversations ({sessions.length})</h1>
          <div className="flex gap-2">
            <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search conversations..." aria-label="Search" className="h-10 rounded-xl border border-ink-200 px-3 text-sm focus:border-brand-500 focus:outline-none" />
            <button onClick={() => setAsc(!asc)} className="h-10 rounded-xl border border-ink-200 bg-white px-3 text-sm text-ink-700">{asc ? "Oldest first" : "Newest first"}</button>
          </div>
        </div>
        <ul className="mt-4 space-y-2">
          {shown.map((s) => (
            <li key={s.id} className="relative">
              <div className="flex items-center rounded-xl border border-ink-100 bg-white shadow-soft hover:border-brand-100">
                <Link to={`/app/c/${s.id}`} className="flex min-w-0 flex-1 items-center justify-between gap-3 px-4 py-3">
                  <span className="truncate text-sm font-medium text-ink-900">{s.pinned ? "📌 " : ""}{s.title}</span>
                  <span className="flex shrink-0 items-center gap-3 text-xs text-ink-500">
                    {s.status === "active" && <span className="rounded-full bg-emergency-50 px-2 py-0.5 font-semibold text-emergency-600">In progress</span>}
                    {new Date(s.updated_at).toLocaleDateString()}
                  </span>
                </Link>
                <button onClick={() => setMenu(menu === s.id ? null : s.id)} aria-label="Chat options" className="mr-2 grid size-9 shrink-0 place-items-center rounded-lg hover:bg-ink-50">
                  <svg viewBox="0 0 24 24" className="size-5" fill="currentColor" aria-hidden="true"><circle cx="12" cy="5" r="1.8" /><circle cx="12" cy="12" r="1.8" /><circle cx="12" cy="19" r="1.8" /></svg>
                </button>
              </div>
              {menu === s.id && (
                <>
                  <div className="fixed inset-0 z-10" onClick={() => setMenu(null)} aria-hidden="true" />
                  <div className="absolute right-2 top-12 z-20 w-56 rounded-xl border border-ink-100 bg-white p-1 shadow-soft">
                    <button className={item} onClick={() => void togglePin(s)}>{s.pinned ? "Unpin chat" : "Pin chat"}</button>
                    <button className={item} disabled={!s.incident_id} onClick={() => navigate(`/app/incident/${s.incident_id}/report`)}>Show handover reports</button>
                    <button className={`${item} text-emergency-600`} onClick={() => void remove(s)}>Delete chat</button>
                  </div>
                </>
              )}
            </li>
          ))}
          {!shown.length && <li className="rounded-xl border border-dashed border-ink-200 p-8 text-center text-sm text-ink-500">No conversations yet.</li>}
        </ul>
      </div>
    </div>
  );
}