import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

/** Phone-only bottom bar (like an Android app) that slides in once the hero has scrolled away. */
export function StickyCta() {
  const [show, setShow] = useState(false);
  useEffect(() => {
    const on = () => setShow(window.scrollY > window.innerHeight * 0.85);
    on();
    window.addEventListener("scroll", on, { passive: true });
    return () => window.removeEventListener("scroll", on);
  }, []);
  return (
    <div className={`fixed inset-x-0 bottom-0 z-40 px-4 pb-[calc(env(safe-area-inset-bottom)+0.75rem)] pt-3 transition-transform duration-300 md:hidden ${show ? "translate-y-0" : "translate-y-full"}`}>
      <div className="flex gap-3 rounded-3xl border border-ink-100 bg-white/90 p-2 shadow-lift backdrop-blur">
        <Link to="/role?next=/signup" className="flex h-12 flex-1 items-center justify-center rounded-2xl bg-brand-600 font-semibold text-white active:scale-[0.98]">Get started free</Link>
        <a href="tel:108" aria-label="Call 108" className="flex h-12 w-14 items-center justify-center rounded-2xl bg-emergency-500 font-bold text-white active:scale-[0.98]">108</a>
      </div>
    </div>
  );
}