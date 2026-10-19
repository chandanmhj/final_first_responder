import { Link } from "react-router-dom";
import { Logo } from "../components/ui/Logo";

const rows = [
  ["IFRC International First Aid, Resuscitation and Education Guidelines 2025", "International Federation of Red Cross and Red Crescent Societies. Used for non-commercial purposes with acknowledgement."],
  ["BCLS Provider Handbook", "RGUHS-JeevaRaksha Trust. Basic life support and common emergency protocols, used with the knowledge and consent of the authors."],
  ["General first-aid guidance (authored)", "Used where the sources above are silent, for example scorpion stings. Marked 'not yet medically reviewed' on the step."],
  ["Hospital data", "Compiled by the project author from public listings. Capabilities shown as 'inferred' are guessed from names."],
];

export default function AboutPage() {
  return (
    <div className="mx-auto max-w-3xl px-5 py-10">
      <Link to="/"><Logo /></Link>
      <h1 className="mt-10 text-3xl font-bold text-ink-950">Sources</h1>
      <p className="mt-2 text-ink-500">Every step shows where it comes from. This app gives decision support and does not replace emergency services or a doctor.</p>
      <ul className="mt-8 space-y-4">{rows.map(([t, d]) => <li key={t} className="rounded-2xl border border-ink-100 bg-white p-5 shadow-soft"><p className="font-display font-bold text-ink-950">{t}</p><p className="mt-1 text-sm text-ink-500">{d}</p></li>)}</ul>
    </div>
  );
}
