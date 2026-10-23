import { lazy, Suspense, useRef, type MouseEvent } from "react";
import { Link } from "react-router-dom";

const Scene3D = lazy(() => import("./Scene3D"));

const HEADLINE = "Calm, correct help when every second counts.".split(" ");
const PILLS = ["Guideline-grounded", "Hands-free voice", "Photo help", "Handover report"];

/** Glass step card that tilts toward the pointer. */
function TiltCard() {
  const ref = useRef<HTMLDivElement>(null);
  const move = (e: MouseEvent) => {
    const el = ref.current;
    if (!el) return;
    const r = el.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - 0.5;
    const y = (e.clientY - r.top) / r.height - 0.5;
    el.style.transform = `perspective(900px) rotateY(${x * 16}deg) rotateX(${-y * 16}deg) scale(1.02)`;
  };
  const leave = () => { if (ref.current) ref.current.style.transform = "perspective(900px) rotateY(0) rotateX(0)"; };
  return (
    <div className="fr-float hidden lg:block">
      <div ref={ref} onMouseMove={move} onMouseLeave={leave} aria-hidden="true"
        className="w-72 rounded-3xl border border-white/15 bg-white/10 p-5 shadow-2xl backdrop-blur-xl transition-transform duration-200 ease-out">
        <div className="mb-3 flex items-center justify-between">
          <span className="rounded-full bg-brand-500/25 px-3 py-1 text-xs font-bold text-brand-100">Step 3 of 8</span>
          <span className="h-1.5 w-20 rounded-full bg-white/15"><span className="block h-full w-1/3 rounded-full bg-brand-500" /></span>
        </div>
        <p className="font-display text-lg font-semibold leading-snug text-white">Press hard and fast in the middle of the chest, about two pushes every second.</p>
        <div className="mt-4 flex gap-2">
          <span className="flex h-10 flex-1 items-center justify-center rounded-xl bg-brand-600 text-xs font-semibold text-white">Done, next step</span>
          <span className="flex h-10 flex-1 items-center justify-center rounded-xl border border-emergency-500/50 bg-emergency-500/15 text-xs font-semibold text-red-200">That didn't work</span>
        </div>
      </div>
    </div>
  );
}

/** Full-screen 3D hero: beating heart scene, animated headline, ECG line and a tilting preview card. */
export function Hero() {
  return (
    <section className="relative isolate min-h-[100svh] overflow-hidden bg-ink-950 text-white">
      <div className="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_72%_42%,rgb(36_88_224/0.38),transparent_58%),radial-gradient(ellipse_at_20%_90%,rgb(229_56_59/0.18),transparent_55%)]" />
      <div className="pointer-events-none absolute inset-0 -z-10 bg-[linear-gradient(rgb(255_255_255/0.045)_1px,transparent_1px),linear-gradient(90deg,rgb(255_255_255/0.045)_1px,transparent_1px)] bg-[size:56px_56px] [mask-image:radial-gradient(ellipse_at_center,black,transparent_75%)]" />

      <Suspense fallback={null}><Scene3D /></Suspense>

      <div className="relative z-10 mx-auto flex min-h-[100svh] max-w-6xl flex-col justify-center px-5 pb-28 pt-32 lg:pt-24">
        <div className="max-w-xl">
          <span className="fr-fade inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-bold text-red-200 backdrop-blur" style={{ animationDelay: "0.05s" }}>
            <span className="size-1.5 animate-pulse rounded-full bg-emergency-500" />Emergency first-aid guide
          </span>
          <h1 className="mt-5 text-5xl font-extrabold leading-[1.04] sm:text-6xl [perspective:800px]">
            {HEADLINE.map((w, i) => (
              <span key={i} className={`fr-word mr-[0.25em] ${i > 2 ? "fr-gradient-text" : ""}`} style={{ animationDelay: `${0.2 + i * 0.08}s` }}>{w}</span>
            ))}
          </h1>
          <p className="fr-fade mt-5 max-w-lg text-lg text-ink-300" style={{ animationDelay: "0.95s" }}>
            Tell it what happened, or send a photo. Get one clear step at a time, by text or voice, and a handover report ready for the ambulance team.
            <br />
             an initiative built by chandan, dhanyatha, muttu, kavana under the guidence of Vishwanath Rajput
          </p>
          <div className="fr-fade mt-8 flex flex-wrap gap-3" style={{ animationDelay: "1.1s" }}>
            <Link to="/role?next=/signup" className="fr-glow-btn inline-flex h-12 items-center rounded-xl bg-brand-600 px-7 font-semibold text-white transition hover:-translate-y-0.5 hover:bg-brand-500">Get started free</Link>
            <a href="tel:108" className="inline-flex h-12 items-center rounded-xl border border-white/20 bg-white/10 px-7 font-semibold text-white backdrop-blur transition hover:-translate-y-0.5 hover:bg-white/20">Emergency? Call 108</a>
          </div>
          <div className="fr-fade mt-8 flex flex-wrap gap-2" style={{ animationDelay: "1.25s" }}>
            {PILLS.map((p) => <span key={p} className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-ink-300">{p}</span>)}
          </div>
        </div>
        <div className="absolute bottom-24 right-5 z-10 xl:right-0"><TiltCard /></div>
      </div>

      <svg className="pointer-events-none absolute inset-x-0 bottom-10 z-0 h-16 w-full" viewBox="0 0 1200 60" preserveAspectRatio="none" aria-hidden="true">
        <path d="M0 30 H430 l14 0 l12 -22 l16 46 l14 -34 l10 10 H1200" fill="none" stroke="rgb(255 255 255 / 0.12)" strokeWidth="1.5" vectorEffect="non-scaling-stroke" />
        <path className="fr-ecg-path" pathLength={1} d="M0 30 H430 l14 0 l12 -22 l16 46 l14 -34 l10 10 H1200" fill="none" stroke="#ff5a5d" strokeWidth="2.5" strokeLinecap="round" vectorEffect="non-scaling-stroke" />
      </svg>

      <div className="absolute inset-x-0 bottom-3 z-10 flex justify-center" aria-hidden="true">
        <span className="flex h-8 w-5 justify-center rounded-full border border-white/30 pt-1.5"><span className="fr-scroll-dot size-1.5 rounded-full bg-white" /></span>
      </div>
    </section>
  );
}