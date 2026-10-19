export function Safety() {
  return (
    <section id="safety" className="mx-auto max-w-6xl px-5 py-20">
      <h2 className="text-3xl font-bold text-ink-950">Safety first, and honest about limits</h2>
      <div className="mt-8 grid gap-5 md:grid-cols-3">
        {[["Always call 108", "A call button is always on screen. This app supports you. It does not replace emergency services or a doctor."], ["Photos are a best guess", "A photo cannot confirm that an animal is safe. After any bite or sting, visit a hospital to be sure."], ["It says when it does not know", "If the guidelines do not cover a question, it tells you and points you to 108 or a doctor."]].map(([t, d]) => (
          <div key={t} className="rounded-2xl border border-ink-100 bg-white p-6 shadow-soft"><h3 className="font-display text-lg font-bold text-ink-950">{t}</h3><p className="mt-2 text-sm text-ink-500">{d}</p></div>
        ))}
      </div>
    </section>
  );
}
