import type { Role } from "../../types/chat";

type Props = { value: Role | null; onChange: (r: Role) => void };

const OPTIONS: { id: Role; title: string; text: string; icon: string }[] = [
  { id: "common", title: "Common person", text: "I am not trained. Explain every step in simple words so I understand what to do.", icon: "🙂" },
  { id: "responder", title: "Certified first responder", text: "I am trained (first aid, BLS or similar). Give me clinical wording and responder-level steps.", icon: "🩺" },
];

/** Two large cards: who is using the app. Wording and steps depend on this choice. */
export function RoleSelector({ value, onChange }: Props) {
  return (
    <div className="grid gap-4 sm:grid-cols-2" role="radiogroup" aria-label="Who are you?">
      {OPTIONS.map((o) => {
        const on = value === o.id;
        return (
          <button
            key={o.id}
            type="button"
            role="radio"
            aria-checked={on}
            onClick={() => onChange(o.id)}
            className={`rounded-2xl border-2 bg-white p-6 text-left shadow-soft transition-all ${on ? "border-brand-600 ring-4 ring-brand-100" : "border-ink-100 hover:border-ink-300"}`}
          >
            <span className="text-3xl" aria-hidden="true">{o.icon}</span>
            <span className="mt-3 block font-display text-xl font-bold text-ink-950">{o.title}</span>
            <span className="mt-1 block text-sm text-ink-500">{o.text}</span>
          </button>
        );
      })}
    </div>
  );
}
