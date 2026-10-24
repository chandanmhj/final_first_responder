import { Reveal, useInView } from "./Reveal";

const steps = [
  ["1", "Say who you are", "Common person or certified first responder. Words and steps match what you know."],
  ["2", "Describe or show", "Type, speak, or send a photo, for example of a bite or an injury."],
  ["3", "Follow one step at a time", "Tap Next when done, or say a step did not work. Short clips show what to do."],
  ["4", "Hand over", "Find the right hospital and give the ambulance team a timed report of what you did."],
];

/** Vertical timeline on phones, four columns on wide screens. */
export function HowItWorks() {
  const [ref, seen] = useInView<HTMLDivElement>(0.2);
  return (
    <section id="how" className="mx-auto max-w-6xl px-6 py-16 sm:py-24">
      <Reveal><h2 className="text-3xl font-bold text-ink-950 sm:text-4xl">How it works</h2></Reveal>
      <div ref={ref} className="relative mt-10">
        <div className="absolute bottom-6 left-5 top-6 w-0.5 rounded-full bg-ink-100 lg:hidden">
          <div className="w-full rounded-full bg-gradient-to-b from-brand-500 to-emergency-500 transition-[height] duration-[1800ms] ease-out" style={{ height: seen ? "100%" : "0%" }} />
        </div>
        <div className="absolute left-[12%] right-[12%] top-5 hidden h-0.5 rounded-full bg-ink-100 lg:block">
          <div className="h-full rounded-full bg-gradient-to-r from-brand-500 to-emergency-500 transition-[width] duration-[1800ms] ease-out" style={{ width: seen ? "100%" : "0%" }} />
        </div>
        <div className="grid gap-7 lg:grid-cols-4 lg:gap-5">
          {steps.map(([n, t, d], i) => (
            <Reveal key={n} delay={i * 120}>
              <div className="flex gap-4 lg:block">
                <span className="relative z-10 grid size-10 shrink-0 place-items-center rounded-xl bg-brand-600 font-bold text-white shadow-lift">{n}</span>
                <div className="lg:mt-4">
                  <h3 className="text-lg font-bold text-ink-950">{t}</h3>
                  <p className="mt-1 text-sm text-ink-500">{d}</p>
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}