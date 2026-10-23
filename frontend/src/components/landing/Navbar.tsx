import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Logo } from "../ui/Logo";

const links = [["How it works", "#how"], ["Features", "#features"], ["Voice", "#voice"], ["Safety", "#safety"], ["FAQ", "#faq"]];

/** Transparent over the 3D hero, turns into a frosted white bar after scrolling. */
export function Navbar() {
  const [solid, setSolid] = useState(false);
  useEffect(() => {
    const on = () => setSolid(window.scrollY > 40);
    on();
    window.addEventListener("scroll", on, { passive: true });
    return () => window.removeEventListener("scroll", on);
  }, []);
  return (
    <header className={`fixed inset-x-0 top-0 z-40 border-b transition-all duration-300 ${solid ? "border-ink-100 bg-white/85 shadow-soft backdrop-blur" : "border-transparent bg-transparent"}`}>
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-5">
        <Link to="/"><Logo invert={!solid} /></Link>
        <nav className={`hidden items-center gap-7 text-sm font-medium md:flex ${solid ? "text-ink-700" : "text-white/80"}`}>
          {links.map(([l, h]) => <a key={h} href={h} className={solid ? "hover:text-brand-600" : "hover:text-white"}>{l}</a>)}
        </nav>
        <div className="flex items-center gap-2">
          <Link to="/role?next=/login" className={`rounded-xl px-4 py-2 text-sm font-semibold ${solid ? "text-ink-700 hover:bg-ink-100" : "text-white hover:bg-white/10"}`}>Log in</Link>
          <Link to="/role?next=/signup" className="rounded-xl bg-brand-600 px-4 py-2 text-sm font-semibold text-white shadow-soft transition hover:-translate-y-0.5 hover:bg-brand-700">Sign up</Link>
        </div>
      </div>
    </header>
  );
}