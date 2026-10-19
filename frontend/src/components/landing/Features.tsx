const items = [
  ["Grounded in guidelines", "Answers come from first-aid guidelines, with the source shown on every step."],
  ["Photo help", "Send a photo with a message, such as a snake or scorpion bite. You get a best guess with a confidence level, and always advice to see a hospital."],
  ["Hands-free voice", "Talk like a call. It listens and speaks at the same time, and knows when you have finished."],
  ["Right hospital, not just nearest", "Hospitals are ranked for the emergency: heart, stroke, trauma, burns, and more."],
  ["Handover report", "A timed record of what happened, in the ISBAR format ambulance teams use."],
  ["Simple or clinical wording", "Plain words for everyone. Clinical terms for certified first responders."],
];

export function Features() {
  return (
    <section id="features" className="bg-ink-50 py-20">
      <div className="mx-auto max-w-6xl px-5">
        <h2 className="text-3xl font-bold text-ink-950">Built for the worst minutes of someone's day</h2>
        <div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {items.map(([t, d]) => (
            <div key={t} className="rounded-2xl border border-ink-100 bg-white p-6 shadow-soft"><h3 className="font-display text-lg font-bold text-ink-950">{t}</h3><p className="mt-2 text-sm text-ink-500">{d}</p></div>
          ))}
        </div>
      </div>
    </section>
  );
}
