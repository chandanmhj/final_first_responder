import { createContext, useCallback, useContext, useMemo, useState } from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useProfile } from "../../hooks/useProfile";
import { EmergencyCallBanner } from "./EmergencyCallBanner";
import { Sidebar } from "./Sidebar";

const ShellCtx = createContext<{ refreshSessions: () => void }>({ refreshSessions: () => undefined });
export const useShell = () => useContext(ShellCtx);

/** Signed-in layout: sidebar plus content, with the call-108 button always in reach. */
export function AppShell() {
  const { loading, needsRole, error } = useProfile();
  const [open, setOpen] = useState(false);
  const [key, setKey] = useState(0);
  const refreshSessions = useCallback(() => setKey((k) => k + 1), []);
  const ctx = useMemo(() => ({ refreshSessions }), [refreshSessions]);

  if (loading) return <div className="grid min-h-dvh place-items-center text-sm text-ink-500">Loading your account...</div>;
  if (needsRole) return <Navigate to="/role?next=/app" replace />;
  return (
    <ShellCtx.Provider value={ctx}>
      <div className="flex h-dvh bg-ink-50">
        <Sidebar open={open} onClose={() => setOpen(false)} refreshKey={key} />
        <div className="flex min-w-0 flex-1 flex-col">
          <header className="flex h-14 shrink-0 items-center gap-3 border-b border-ink-100 bg-white px-4 pt-[env(safe-area-inset-top)]">
            <button className="grid size-9 place-items-center rounded-lg hover:bg-ink-50 lg:hidden" onClick={() => setOpen(true)} aria-label="Open menu">
              <svg viewBox="0 0 24 24" className="size-5" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16" /></svg>
            </button>
            <p className="flex-1 truncate text-sm text-ink-500">{error ?? "Decision support only. In an emergency, call 108."}</p>
            <EmergencyCallBanner />
          </header>
          <main className="flex min-h-0 flex-1 flex-col"><Outlet /></main>
        </div>
      </div>
    </ShellCtx.Provider>
  );
}