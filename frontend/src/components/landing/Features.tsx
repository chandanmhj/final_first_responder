import { Reveal } from "./Reveal";

const items = [
  ["Grounded in guidelines", "Answers come from first-aid guidelines, with the source shown on every step."],
  ["Photo help", "Send a photo with a message, such as a snake or scorpion bite. You get a best guess with a confidence level, and always advice to see a hospital."],
  ["Hands-free voice", "Talk like a call. It listens and speaks at the same time, and knows when you have finished."],
  ["Right hospital, not just nearest", "Hospitals are ranked for the emergency: heart, stroke, trauma, burns, and more."],
  ["Handover report", "A timed record of what happened, in the ISBAR format ambulance teams use."],
  ["Simple or clinical wording", "Plain words for everyone. Clinical terms for certified first responders."],
];

/** Swipeable cards on phones, a grid on wide screens. */
export function Features() {
  return (
    <section id="features" className="bg-ink-50 py-16 sm:py-24">
      <div className="mx-auto max-w-6xl">
        <Reveal><h2 className="px-6 text-3xl font-bold text-ink-950 sm:text-4xl">Built for the worst minutes of someone's day</h2></Reveal>
        <div className="no-scrollbar mt-8 flex snap-x snap-mandatory gap-4 overflow-x-auto px-6 pb-4 md:grid md:grid-cols-2 md:overflow-visible md:pb-0 lg:grid-cols-3">
          {items.map(([t, d], i) => (
            <div key={t} className="w-[78%] shrink-0 snap-center sm:w-[60%] md:w-auto">
              <Reveal delay={i * 80} className="h-full">
                <div className="h-full rounded-3xl border border-ink-100 bg-white p-6 shadow-soft transition duration-300 lg:hover:-translate-y-1 lg:hover:shadow-lift">
                  <span className="mb-4 block h-1 w-10 rounded-full bg-gradient-to-r from-brand-500 to-emergency-500" />
                  <h3 className="font-display text-lg font-bold text-ink-950">{t}</h3>
                  <p className="mt-2 text-sm text-ink-500">{d}</p>
                </div>
              </Reveal>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}