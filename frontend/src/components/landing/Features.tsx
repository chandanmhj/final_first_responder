import type { MouseEvent } from "react";
import { Reveal } from "./Reveal";

const items = [
  ["Grounded in guidelines", "Answers come from first-aid guidelines, with the source shown on every step."],
  ["Photo help", "Send a photo with a message, such as a snake or scorpion bite. You get a best guess with a confidence level, and always advice to see a hospital."],
  ["Hands-free voice", "Talk like a call. It listens and speaks at the same time, and knows when you have finished."],
  ["Right hospital, not just nearest", "Hospitals are ranked for the emergency: heart, stroke, trauma, burns, and more."],
  ["Handover report", "A timed record of what happened, in the ISBAR format ambulance teams use."],
  ["Simple or clinical wording", "Plain words for everyone. Clinical terms for certified first responders."],
];

/** Card with a light that follows the pointer and a slight 3D tilt. */
function SpotCard({ title, text }: { title: string; text: string }) {
  const move = (e: MouseEvent<HTMLDivElement>) => {
    const el = e.currentTarget;
    const r = el.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width;
    const y = (e.clientY - r.top) / r.height;
    el.style.setProperty("--mx", `${x * 100}%`);
    el.style.setProperty("--my", `${y * 100}%`);
    el.style.transform = `perspective(800px) rotateY(${(x - 0.5) * 8}deg) rotateX(${(0.5 - y) * 8}deg) translateY(-4px)`;
  };
  const leave = (e: MouseEvent<HTMLDivElement>) => { e.currentTarget.style.transform = ""; };
  return (
    <div onMouseMove={move} onMouseLeave={leave} className="fr-spot h-full rounded-2xl border border-ink-100 bg-white p-6 shadow-soft transition-[transform,box-shadow] duration-200 ease-out hover:shadow-lift">
      <span className="mb-3 block h-1 w-8 rounded-full bg-gradient-to-r from-brand-500 to-emergency-500" />
      <h3 className="font-display text-lg font-bold text-ink-950">{title}</h3>
      <p className="mt-2 text-sm text-ink-500">{text}</p>
    </div>
  );
}

export function Features() {
  return (
    <section id="features" className="bg-ink-50 py-24">
      <div className="mx-auto max-w-6xl px-5">
        <Reveal><h2 className="text-3xl font-bold text-ink-950 sm:text-4xl">Built for the worst minutes of someone's day</h2></Reveal>
        <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {items.map(([t, d], i) => <Reveal key={t} delay={(i % 3) * 120 + Math.floor(i / 3) * 80}><SpotCard title={t} text={d} /></Reveal>)}
        </div>
      </div>
    </section>
  );
}