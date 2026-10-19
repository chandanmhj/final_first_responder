export function TypingIndicator() {
  return (
    <div className="flex w-fit items-center gap-1.5 rounded-2xl rounded-bl-md bg-white px-4 py-3 shadow-soft" role="status" aria-label="First Responder is typing">
      {[0, 150, 300].map((d) => (
        <span key={d} className="size-2 animate-bounce rounded-full bg-ink-300" style={{ animationDelay: `${d}ms` }} />
      ))}
    </div>
  );
}
