import { lazy, Suspense } from "react";
import { Link } from "react-router-dom";

const Scene3D = lazy(() => import("./Scene3D"));

const HEADLINE = "Calm, correct help when every second counts.".split(" ");

/** Phone-first 3D hero: heart on top, short headline and one big button below. */
export function Hero() {
  return (
    <section className="relative isolate flex min-h-[100svh] flex-col justify-end overflow-hidden bg-ink-950 text-white lg:justify-center">
      <div className="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_50%_28%,rgb(36_88_224/0.42),transparent_62%),radial-gradient(ellipse_at_50%_100%,rgb(229_56_59/0.2),transparent_55%)] lg:bg-[radial-gradient(ellipse_at_72%_45%,rgb(36_88_224/0.4),transparent_58%)]" />

      <Suspense fallback={null}><Scene3D /></Suspense>

      <div className="relative z-10 mx-auto w-full max-w-6xl px-6 pb-[calc(env(safe-area-inset-bottom)+2rem)] pt-24">
        <div className="max-w-xl">
          <span className="fr-fade inline-flex items-center gap-2 rounded-full bg-white/10 px-3 py-1.5 text-xs font-semibold text-red-200 backdrop-blur" style={{ animationDelay: "0.05s" }}>
            <span className="size-1.5 animate-pulse rounded-full bg-emergency-500" />first-aid guide
          </span>
          <h1 className="mt-4 text-[2.35rem] font-extrabold leading-[1.08] sm:text-6xl [perspective:800px]">
            {HEADLINE.map((w, i) => (
              <span key={i} className={`fr-word mr-[0.25em] ${i > 2 ? "fr-gradient-text" : ""}`} style={{ animationDelay: `${0.15 + i * 0.07}s` }}>{w}</span>
            ))}
          </h1>
          <p className="fr-fade mt-4 text-base text-ink-300 sm:text-lg" style={{ animationDelay: "0.8s" }}>
            Tell it what happened or send a photo. Get one clear step at a time, by text or voice.
            <br />
              An initiative by Dhanyatha and Team under the guidance under the guidence of Vishwanath Rajput
          </p>
          <div className="fr-fade mt-7 flex flex-col gap-3 sm:flex-row" style={{ animationDelay: "0.95s" }}>
            <Link to="/role?next=/signup" className="fr-glow-btn inline-flex h-14 items-center justify-center rounded-2xl bg-brand-600 px-8 text-base font-semibold text-white active:scale-[0.98] lg:hover:bg-brand-500">Get started free</Link>
            <a href="tel:108" className="inline-flex h-14 items-center justify-center rounded-2xl border border-white/20 bg-white/10 px-8 text-base font-semibold text-white backdrop-blur active:scale-[0.98] lg:hover:bg-white/20">Emergency? Call 108</a>
          </div>
        </div>
      </div>
    </section>
  );
}