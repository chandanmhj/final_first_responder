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
  const [age, setAge] = useState(profile?.age?.toString() ?? "");
  const [sex, setSex] = useState(profile?.sex ?? "");
  const [blood, setBlood] = useState(profile?.blood_group ?? "");
  const [allergies, setAllergies] = useState(profile?.allergies ?? "");
  const [conditions, setConditions] = useState(profile?.conditions ?? "");
  const [meds, setMeds] = useState(profile?.medications ?? "");
  const [contact, setContact] = useState(profile?.emergency_contact ?? "");
  const [msg, setMsg] = useState<string | null>(null);

  const save = async () => {
    try {
      await api.putMe({
        full_name: name || undefined, role: role ?? undefined, attested: role === "responder" ? attested : undefined,
        age: age ? Number(age) : undefined, sex: sex || undefined, blood_group: blood || undefined, allergies: allergies || undefined,
        conditions: conditions || undefined, medications: meds || undefined, emergency_contact: contact || undefined,
      });
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
      <section className="space-y-4 rounded-2xl border border-ink-100 bg-white p-5 shadow-soft">
        <div>
          <h2 className="font-display text-lg font-bold text-ink-950">Medical details</h2>
          <p className="text-xs text-ink-500">Shown to paramedics in the handover report only when you choose "this is for me" in a chat.</p>
        </div>
        <div className="grid gap-4 sm:grid-cols-3">
          <Input label="Age" type="number" min={0} max={120} value={age} onChange={(e) => setAge(e.target.value)} />
          <div className="space-y-1.5">
            <label htmlFor="sex" className="block text-sm font-medium text-ink-700">Sex</label>
            <select id="sex" value={sex} onChange={(e) => setSex(e.target.value)} className="h-11 w-full rounded-xl border border-ink-200 bg-white px-3 text-sm focus:border-brand-500 focus:outline-none focus:ring-4 focus:ring-brand-100">
              <option value="">Select</option><option>Male</option><option>Female</option><option>Other</option><option>Prefer not to say</option>
            </select>
          </div>
          <Input label="Blood group" placeholder="e.g. O+" value={blood} onChange={(e) => setBlood(e.target.value)} />
        </div>
        <Input label="Allergies" placeholder="e.g. penicillin, peanuts" value={allergies} onChange={(e) => setAllergies(e.target.value)} />
        <Input label="Medical conditions" placeholder="e.g. diabetes, asthma" value={conditions} onChange={(e) => setConditions(e.target.value)} />
        <Input label="Current medicines" value={meds} onChange={(e) => setMeds(e.target.value)} />
        <Input label="Emergency contact" placeholder="Name and phone" value={contact} onChange={(e) => setContact(e.target.value)} />
      </section>
      <div className="flex items-center gap-3"><Button onClick={() => void save()} disabled={role === "responder" && !attested}>Save</Button>{msg && <span className="text-sm text-ink-500">{msg}</span>}</div>
    </div></div>
  );
}