import { useEffect, useMemo, useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import { useProfile } from "../../hooks/useProfile";
import { api } from "../../lib/api";
import { roleLabel } from "../../lib/role";
import type { SessionSummary } from "../../types/chat";
import { Logo } from "../ui/Logo";

type Props = { open: boolean; onClose: () => void; refreshKey: number };

const nav = [
  { to: "/app", label: "Conversations", end: true, icon: "M4 5h16v11H8l-4 4z" },
  { to: "/app/hospitals", label: "Hospitals", end: false, icon: "M5 21V8l7-5 7 5v13M9 21v-6h6v6M12 9v3M10.5 10.5h3" },
  { to: "/app/reports", label: "Handover reports", end: false, icon: "M7 3h8l4 4v14H7zM15 3v4h4M10 12h6M10 16h6" },
  { to: "/app/profile", label: "Profile", end: false, icon: "M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21a8 8 0 0 1 16 0" },
];

/** Left navigation like the Figma chat design: profile, search, sections, recent conversations, new conversation. */
export function Sidebar({ open, onClose, refreshKey }: Props) {
  const { user, signOut } = useAuth();
  const { profile } = useProfile();
  const navigate = useNavigate();
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [q, setQ] = useState("");

  useEffect(() => {
    let alive = true;
    api.listSessions().then((s) => alive && setSessions(s)).catch(() => undefined);
    return () => {
      alive = false;
    };
  }, [refreshKey]);

  const shown = useMemo(() => sessions.filter((s) => s.title.toLowerCase().includes(q.toLowerCase())).slice(0, 12), [sessions, q]);
  const name = profile?.full_name || (user?.user_metadata?.full_name as string | undefined) || user?.email || "You";
  const initials = name.split(/\s+/).map((p) => p[0]).slice(0, 2).join("").toUpperCase();

  return (
    <>
      {open && <div className="fixed inset-0 z-30 bg-ink-950/40 lg:hidden" onClick={onClose} aria-hidden="true" />}
      <aside className={`fixed inset-y-0 left-0 z-40 flex w-72 flex-col border-r border-ink-100 bg-white p-4 transition-transform lg:static lg:translate-x-0 ${open ? "translate-x-0" : "-translate-x-full"}`}>
        <div className="flex items-center justify-between">
          <Logo />
        </div>
        <div className="mt-5 flex items-center gap-3 rounded-xl bg-ink-50 p-3">
          <span className="grid size-9 place-items-center rounded-full bg-brand-600 text-sm font-bold text-white">{initials}</span>
          <div className="min-w-0">
            <p className="truncate text-sm font-semibold text-ink-950">{name}</p>
            <p className="truncate text-xs text-ink-500">{roleLabel(profile?.role)}</p>
          </div>
        </div>
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search conversations..." aria-label="Search conversations" className="mt-4 h-10 rounded-xl border border-ink-200 px-3 text-sm placeholder:text-ink-300 focus:border-brand-500 focus:outline-none focus:ring-4 focus:ring-brand-100" />
        <nav className="mt-4 space-y-1">
          {nav.map((n) => (
            <NavLink key={n.to} to={n.to} end={n.end} onClick={onClose} className={({ isActive }) => `flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium ${isActive ? "bg-ink-900 text-white" : "text-ink-700 hover:bg-ink-50"}`}>
              <svg viewBox="0 0 24 24" className="size-4" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d={n.icon} /></svg>
              {n.label}
            </NavLink>
          ))}
        </nav>
        <p className="mt-5 px-3 text-[11px] font-semibold uppercase tracking-widest text-ink-300">Recent</p>
        <div className="mt-1 min-h-0 flex-1 space-y-0.5 overflow-y-auto">
          {shown.map((s) => (
            <NavLink key={s.id} to={`/app/c/${s.id}`} onClick={onClose} className={({ isActive }) => `block truncate rounded-lg px-3 py-2 text-sm ${isActive ? "bg-brand-50 text-brand-700" : "text-ink-700 hover:bg-ink-50"}`}>
              {s.title}
            </NavLink>
          ))}
          {!shown.length && <p className="px-3 py-2 text-xs text-ink-500">No conversations yet.</p>}
        </div>
        <button onClick={() => { onClose(); navigate("/app/c/new"); }} className="mt-3 h-11 rounded-xl bg-brand-600 text-sm font-semibold text-white shadow-soft hover:bg-brand-700">
          + Start a new conversation
        </button>
        <button onClick={() => void signOut()} className="mt-2 h-9 rounded-xl text-xs font-semibold text-ink-500 hover:bg-ink-50">Log out</button>
      </aside>
    </>
  );
}
