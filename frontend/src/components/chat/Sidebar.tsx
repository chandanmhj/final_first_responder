import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import { useProfile } from "../../hooks/useProfile";
import { roleLabel } from "../../lib/role";
import { Logo } from "../ui/Logo";

type Props = { open: boolean; onClose: () => void };

const icon = "size-4";
const svgProps = { viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 2, strokeLinecap: "round", strokeLinejoin: "round", "aria-hidden": true } as const;
const row = "flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-sm font-medium";

/** Left menu with only: New chat, Previous conversations, Profile. The X closes it. */
export function Sidebar({ open, onClose }: Props) {
  const { user, signOut } = useAuth();
  const { profile } = useProfile();
  const navigate = useNavigate();
  const name = profile?.full_name || (user?.user_metadata?.full_name as string | undefined) || user?.email || "You";
  const initials = name.split(/\s+/).map((p) => p[0]).slice(0, 2).join("").toUpperCase();
  const closeOnMobile = () => { if (window.innerWidth < 1024) onClose(); };
  const active = ({ isActive }: { isActive: boolean }) => `${row} ${isActive ? "bg-ink-900 text-white" : "text-ink-700 hover:bg-ink-50"}`;

  return (
    <>
      {open && <div className="fixed inset-0 z-30 bg-ink-950/40 lg:hidden" onClick={onClose} aria-hidden="true" />}
      <aside className={`${open ? "flex" : "hidden"} fixed inset-y-0 left-0 z-40 w-72 flex-col border-r border-ink-100 bg-white p-4 lg:static`}>
        <div className="flex items-center justify-between">
          <Logo />
          <button onClick={onClose} aria-label="Close sidebar" className="grid size-9 place-items-center rounded-lg hover:bg-ink-50">
            <svg {...svgProps} className="size-5"><path d="M6 6l12 12M18 6L6 18" /></svg>
          </button>
        </div>
        <div className="mt-5 flex items-center gap-3 rounded-xl bg-ink-50 p-3">
          <span className="grid size-9 place-items-center rounded-full bg-brand-600 text-sm font-bold text-white">{initials}</span>
          <div className="min-w-0">
            <p className="truncate text-sm font-semibold text-ink-950">{name}</p>
            <p className="truncate text-xs text-ink-500">{roleLabel(profile?.role)}</p>
          </div>
        </div>
        <nav className="mt-5 space-y-1">
          <button onClick={() => { closeOnMobile(); navigate("/app/c/new", { state: { fresh: Date.now() } }); }} className={`${row} bg-brand-600 text-white hover:bg-brand-700`}>
            <svg {...svgProps} className={icon}><path d="M12 5v14M5 12h14" /></svg>New chat
          </button>
          <NavLink to="/app" end onClick={closeOnMobile} className={active}>
            <svg {...svgProps} className={icon}><path d="M4 5h16v11H8l-4 4z" /></svg>Previous conversations
          </NavLink>
          <NavLink to="/app/profile" onClick={closeOnMobile} className={active}>
            <svg {...svgProps} className={icon}><path d="M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21a8 8 0 0 1 16 0" /></svg>Profile
          </NavLink>
        </nav>
        <div className="flex-1" />
        <button onClick={() => void signOut()} className="mt-2 h-9 rounded-xl text-xs font-semibold text-ink-500 hover:bg-ink-50">Log out</button>
      </aside>
    </>
  );
}