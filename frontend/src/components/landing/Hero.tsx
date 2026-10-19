import { Link } from "react-router-dom";

/** Headline, call to action, and a small preview of a step card. */
export function Hero() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-brand-50 to-white">
      <div className="pointer-events-none absolute -right-24 -top-24 size-96 rounded-full bg-emergency-500/10 blur-3xl" />
      <div className="mx-auto grid max-w-6xl items-center gap-12 px-5 py-20 lg:grid-cols-2">
        <div>
          <span className="rounded-full bg-white px-3 py-1 text-xs font-bold text-emergency-600 shadow-soft">Emergency first-aid guide</span>
          <h1 className="mt-5 text-5xl font-extrabold leading-[1.05] text-ink-950 sm:text-6xl">Calm, correct help when every second counts.</h1>
          <p className="mt-5 max-w-lg text-lg text-ink-500">Tell it what happened, or send a photo. Get one clear step at a time, by text or voice, and a handover report ready for the ambulance team.</p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link to="/role?next=/signup" className="inline-flex h-12 items-center rounded-xl bg-brand-600 px-7 font-semibold text-white shadow-lift hover:bg-brand-700">Get started free</Link>
            <a href="tel:108" className="inline-flex h-12 items-center rounded-xl border border-emergency-500/40 bg-white px-7 font-semibold text-emergency-600 hover:bg-emergency-50">Emergency? Call 108</a>
          </div>
        </div>
        <div className="mx-auto w-full max-w-sm rounded-3xl border border-ink-100 bg-white p-5 shadow-lift" aria-hidden="true">
          <div className="mb-3 flex items-center justify-between"><span className="rounded-full bg-brand-50 px-3 py-1 text-xs font-bold text-brand-700">Step 3 of 8</span><span className="h-1.5 w-20 rounded-full bg-ink-100"><span className="block h-full w-1/3 rounded-full bg-brand-500" /></span></div>
          <p className="font-display text-xl font-semibold text-ink-950">Press hard and fast in the middle of the chest, about two pushes every second.</p>
          <div className="mt-4 grid aspect-video place-items-center rounded-2xl bg-ink-950 text-xs text-ink-300">short video plays here</div>
          <div className="mt-4 flex gap-2"><span className="flex h-11 flex-1 items-center justify-center rounded-xl bg-brand-600 text-sm font-semibold text-white">Done, next step</span><span className="flex h-11 flex-1 items-center justify-center rounded-xl border border-emergency-500/40 bg-emergency-50 text-sm font-semibold text-emergency-600">That didn't work</span></div>
        </div>
      </div>
    </section>
  );
}
