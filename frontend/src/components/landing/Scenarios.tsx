const chips = ["Heart attack", "Cardiac arrest", "Stroke", "Choking", "Severe bleeding", "Road accident", "Bike accident and helmet", "Snake bite", "Scorpion sting", "Burns", "Drowning", "Seizure", "Low blood sugar", "Asthma attack", "Allergic reaction", "Poisoning", "Heatstroke", "Fractures", "Head injury", "Childbirth"];

export function Scenarios() {
  return (
    <section className="mx-auto max-w-6xl px-5 py-20">
      <h2 className="text-3xl font-bold text-ink-950">Over 180 situations, safe order built in</h2>
      <p className="mt-2 max-w-2xl text-ink-500">A heart attack on the road starts with getting safe. A road accident where someone is not breathing starts with scene safety, then CPR. The order changes with where you are.</p>
      <div className="mt-8 flex flex-wrap gap-2">{chips.map((c) => <span key={c} className="rounded-full border border-ink-200 bg-white px-4 py-2 text-sm font-medium text-ink-700">{c}</span>)}<span className="rounded-full bg-brand-50 px-4 py-2 text-sm font-semibold text-brand-700">and more</span></div>
    </section>
  );
}
