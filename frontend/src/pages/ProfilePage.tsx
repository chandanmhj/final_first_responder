import { useState } from "react";
import { RoleSelector } from "../components/chat/RoleSelector";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import { useProfile } from "../hooks/useProfile";
import { api } from "../lib/api";
import { setStoredRole } from "../lib/role";
import type { Role } from "../types/chat";

export default function ProfilePage() {
  const { profile, refresh } = useProfile();
  const [name, setName] = useState(profile?.full_name ?? "");
  const [role, setRole] = useState<Role | null>(profile?.role ?? null);
  const [attested, setAttested] = useState(!!profile?.attested_at);
  const [msg, setMsg] = useState<string | null>(null);
  const save = async () => {
    try {
      await api.putMe({ full_name: name || undefined, role: role ?? undefined, attested: role === "responder" ? attested : undefined });
      if (role) setStoredRole({ role, attested, cert: "" });
      await refresh(); setMsg("Saved.");
    } catch (e) { setMsg(e instanceof Error ? e.message : "Could not save."); }
  };
  return (
    <div className="flex-1 overflow-y-auto px-4 py-8 sm:px-10"><div className="mx-auto max-w-2xl space-y-6">
      <h1 className="text-2xl font-bold text-ink-950">Profile</h1>
      <Input label="Name" value={name} onChange={(e) => setName(e.target.value)} />
      <RoleSelector value={role} onChange={setRole} />
      {role === "responder" && <label className="flex items-start gap-3 text-sm text-ink-700"><input type="checkbox" checked={attested} onChange={(e) => setAttested(e.target.checked)} className="mt-0.5 size-5 accent-brand-600" />I confirm I am a trained or certified first responder.</label>}
      <div className="flex items-center gap-3"><Button onClick={() => void save()} disabled={role === "responder" && !attested}>Save</Button>{msg && <span className="text-sm text-ink-500">{msg}</span>}</div>
    </div></div>
  );
}
