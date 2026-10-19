import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import { Logo } from "../ui/Logo";

type Props = {
  title: string;
  subtitle?: string;
  children: ReactNode;
  footer?: ReactNode;
};

const points = [
  "Step-by-step guidance written for the person who is helping",
  "Hands-free voice mode when your hands are busy",
  "A ready handover report when the ambulance arrives",
];

/** Split-screen layout shared by every authentication page. */
export function AuthLayout({ title, subtitle, children, footer }: Props) {
  return (
    <div className="grid min-h-dvh lg:grid-cols-[1.05fr_1fr]">
      <aside className="relative hidden overflow-hidden bg-ink-950 p-12 text-white lg:flex lg:flex-col lg:justify-between">
        <div className="pointer-events-none absolute -right-32 -top-32 size-[28rem] rounded-full bg-brand-600/30 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-40 -left-24 size-[26rem] rounded-full bg-emergency-500/25 blur-3xl" />
        <Link to="/" className="relative w-fit"><Logo invert /></Link>
        <div className="relative max-w-md">
          <h2 className="text-4xl font-bold leading-tight">Calm, correct help when every second counts.</h2>
          <ul className="mt-8 space-y-4 text-ink-200">
            {points.map((p) => (
              <li key={p} className="flex gap-3">
                <span className="mt-0.5 grid size-5 shrink-0 place-items-center rounded-full bg-white/10 text-xs">✓</span>
                {p}
              </li>
            ))}
          </ul>
        </div>
        <p className="relative text-xs text-ink-300">Decision support only. In an emergency, call 108.</p>
      </aside>

      <main className="flex items-center justify-center px-5 py-10 sm:px-8">
        <div className="w-full max-w-md">
          <Link to="/" className="mb-8 block w-fit lg:hidden"><Logo /></Link>
          <h1 className="text-3xl font-bold text-ink-950">{title}</h1>
          {subtitle && <p className="mt-2 text-sm text-ink-500">{subtitle}</p>}
          <div className="mt-8 rounded-2xl border border-ink-100 bg-white p-6 shadow-soft sm:p-7">{children}</div>
          {footer && <div className="mt-6 text-center text-sm text-ink-500">{footer}</div>}
        </div>
      </main>
    </div>
  );
}
