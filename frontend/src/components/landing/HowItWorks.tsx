import { Reveal, useInView } from "./Reveal";

const steps = [
  ["1", "Say who you are", "Common person or certified first responder. Words and steps match what you know."],
  ["2", "Describe or show", "Type, speak, or send a photo, for example of a bite or an injury."],
  ["3", "Follow one step at a time", "Tap Next when done, or tell it that a step did not work. Short clips show what to do."],
  ["4", "Hand over", "Find a suitable hospital and give the ambulance team a timed report of what you did."],
];

export function HowItWorks() {
  const [ref, seen] = useInView<HTMLDivElement>(0.3);
  return (
    <section id="how" className="mx-auto max-w-6xl px-5 py-24">
      <Reveal><h2 className="text-3xl font-bold text-ink-950 sm:text-4xl">How it works</h2></Reveal>
      <div ref={ref} className="relative mt-12">
        <div className="absolute left-[12%] right-[12%] top-5 hidden h-0.5 rounded-full bg-ink-100 lg:block">
          <div className="h-full rounded-full bg-gradient-to-r from-brand-500 to-emergency-500 transition-[width] duration-[1800ms] ease-out" style={{ width: seen ? "100%" : "0%" }} />
        </div>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {steps.map(([n, t, d], i) => (
            <Reveal key={n} delay={i * 140}>
              <div className="group h-full rounded-2xl border border-ink-100 bg-white p-6 shadow-soft transition duration-300 hover:-translate-y-2 hover:shadow-lift">
                <span className="relative z-10 grid size-10 place-items-center rounded-xl bg-brand-600 font-bold text-white shadow-lift transition group-hover:scale-110 group-hover:bg-emergency-500">{n}</span>
                <h3 className="mt-4 text-lg font-bold text-ink-950">{t}</h3>
                <p className="mt-1 text-sm text-ink-500">{d}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}