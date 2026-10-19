/** Always-visible call button. In an emergency the first thing to do is call 108. */
export function EmergencyCallBanner({ urgent }: { urgent?: boolean }) {
  return (
    <a
      href="tel:108"
      className={`inline-flex h-10 items-center gap-2 rounded-xl px-4 text-sm font-bold text-white shadow-soft transition-colors ${urgent ? "animate-pulse bg-emergency-600" : "bg-emergency-500 hover:bg-emergency-600"}`}
      aria-label="Call 108 ambulance"
    >
      <svg viewBox="0 0 24 24" className="size-4" fill="currentColor" aria-hidden="true">
        <path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.6a1 1 0 0 1-.25 1Z" />
      </svg>
      Call 108
    </a>
  );
}
