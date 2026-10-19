type Props = { className?: string; showText?: boolean; invert?: boolean };

/** First Responder logo: a heart with a pulse line, plus the product name. */
export function Logo({ className = "", showText = true, invert = false }: Props) {
  return (
    <span className={`inline-flex items-center gap-2.5 ${className}`}>
      <span className="grid size-9 place-items-center rounded-xl bg-emergency-500 text-white shadow-soft">
        <svg viewBox="0 0 24 24" className="size-5" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M20.8 5.6a5 5 0 0 0-7.1 0L12 7.3l-1.7-1.7a5 5 0 0 0-7.1 7.1L12 21l8.8-8.3a5 5 0 0 0 0-7.1Z" />
          <path d="M7 12h2.2l1.3-2.6 2 5 1.3-2.4H17" />
        </svg>
      </span>
      {showText && (
        <span className={`font-display text-lg font-bold tracking-tight ${invert ? "text-white" : "text-ink-950"}`}>
          First Responder
        </span>
      )}
    </span>
  );
}
