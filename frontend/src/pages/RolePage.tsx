import { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { RoleSelector } from "../components/chat/RoleSelector";
import { Button } from "../components/ui/Button";
import { Logo } from "../components/ui/Logo";
import { getStoredRole, setStoredRole } from "../lib/role";
import type { Role } from "../types/chat";

/** Asked before login: who are you? Saved in the browser, then in the profile after login. */
export default function RolePage() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const next = params.get("next") === "/login" ? "/login" : params.get("next") === "/app" ? "/app" : "/signup";
  const stored = getStoredRole();
  const [role, setRole] = useState<Role | null>(stored?.role ?? null);
  const [attested, setAttested] = useState(stored?.attested ?? false);
  const [cert, setCert] = useState(stored?.cert ?? "");
  const ok = role === "common" || (role === "responder" && attested);

  return (
    <div className="mx-auto flex min-h-dvh max-w-3xl flex-col px-5 py-10">
      <Link to="/" className="w-fit"><Logo /></Link>
      <h1 className="mt-10 text-4xl font-extrabold text-ink-950">Who are you?</h1>
      <p className="mt-2 text-ink-500">This decides the words and steps you see. You can change it later in your profile.</p>
      <div className="mt-8"><RoleSelector value={role} onChange={setRole} /></div>
      {role === "responder" && (
        <div className="mt-5 space-y-4 rounded-2xl border border-ink-100 bg-white p-5 shadow-soft">
          <label className="flex items-start gap-3 text-sm text-ink-700">
            <input type="checkbox" checked={attested} onChange={(e) => setAttested(e.target.checked)} className="mt-0.5 size-5 accent-brand-600" />
            I confirm I am trained or certified in first aid or basic life support, and I understand that medicine and clinical steps are meant for trained people.
          </label>
          <label className="block text-sm font-medium text-ink-700">Certificate number (optional, not verified)
            <input value={cert} onChange={(e) => setCert(e.target.value)} className="mt-1.5 h-11 w-full rounded-xl border border-ink-200 px-3.5 text-sm focus:border-brand-500 focus:outline-none focus:ring-4 focus:ring-brand-100" />
          </label>
        </div>
      )}
      <Button className="mt-8 self-start" disabled={!ok} onClick={() => { setStoredRole({ role: role as Role, attested, cert: cert.trim() }); navigate(next); }}>Continue</Button>
    </div>
  );
}
