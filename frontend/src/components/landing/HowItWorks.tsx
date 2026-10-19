const steps = [
  ["1", "Say who you are", "Common person or certified first responder. Words and steps match what you know."],
  ["2", "Describe or show", "Type, speak, or send a photo, for example of a bite or an injury."],
  ["3", "Follow one step at a time", "Tap Next when done, or tell it that a step did not work. Short clips show what to do."],
  ["4", "Hand over", "Find a suitable hospital and give the ambulance team a timed report of what you did."],
];

export function HowItWorks() {
  return (
    <section id="how" className="mx-auto max-w-6xl px-5 py-20">
      <h2 className="text-3xl font-bold text-ink-950">How it works</h2>
      <div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {steps.map(([n, t, d]) => (
          <div key={n} className="rounded-2xl border border-ink-100 bg-white p-6 shadow-soft">
            <span className="grid size-10 place-items-center rounded-xl bg-brand-600 font-bold text-white">{n}</span>
            <h3 className="mt-4 text-lg font-bold text-ink-950">{t}</h3>
            <p className="mt-1 text-sm text-ink-500">{d}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
