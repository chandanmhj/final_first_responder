import { Link } from "react-router-dom";
import { Logo } from "../ui/Logo";

const links = [["How it works", "#how"], ["Features", "#features"], ["Voice", "#voice"], ["Safety", "#safety"], ["FAQ", "#faq"]];

/** Top bar. Log in and Sign up first ask who you are, then open their own pages. */
export function Navbar() {
  return (
    <header className="sticky top-0 z-30 border-b border-ink-100 bg-white/85 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-5">
        <Link to="/"><Logo /></Link>
        <nav className="hidden items-center gap-7 text-sm font-medium text-ink-700 md:flex">
          {links.map(([l, h]) => <a key={h} href={h} className="hover:text-brand-600">{l}</a>)}
        </nav>
        <div className="flex items-center gap-2">
          <Link to="/role?next=/login" className="rounded-xl px-4 py-2 text-sm font-semibold text-ink-700 hover:bg-ink-100">Log in</Link>
          <Link to="/role?next=/signup" className="rounded-xl bg-brand-600 px-4 py-2 text-sm font-semibold text-white shadow-soft hover:bg-brand-700">Sign up</Link>
        </div>
      </div>
    </header>
  );
}
