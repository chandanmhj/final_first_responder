import { Link } from "react-router-dom";
import { Logo } from "../ui/Logo";

export function Footer() {
  return (
    <footer className="border-t border-ink-100 bg-white py-10">
      <div className="mx-auto flex max-w-6xl flex-col gap-6 px-5 sm:flex-row sm:items-center sm:justify-between">
        <div><Logo /><p className="mt-3 max-w-sm text-xs text-ink-500">Decision support only. It does not replace emergency services or a doctor. In an emergency, call 108.</p></div>
        <nav className="flex gap-6 text-sm font-medium text-ink-700"><Link to="/about">Sources</Link><Link to="/role?next=/login">Log in</Link><Link to="/role?next=/signup">Sign up</Link></nav>
      </div>
    </footer>
  );
}
