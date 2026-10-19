export function VoiceMode() {
  return (
    <section id="voice" className="bg-ink-950 py-20 text-white">
      <div className="mx-auto grid max-w-6xl items-center gap-10 px-5 lg:grid-cols-2">
        <div>
          <h2 className="text-3xl font-bold">Hands busy? Just talk.</h2>
          <p className="mt-3 text-ink-300">Turn on hands-free mode and it works like a call. No buttons to hold. It listens while it speaks, so you can interrupt, and it decides by itself when you have finished.</p>
          <ul className="mt-6 space-y-2 text-sm text-ink-200"><li>Say "next" when a step is done</li><li>Say "it didn't work" if it does not help</li><li>Say "show hospitals" to find the nearest suitable one</li></ul>
        </div>
        <div className="mx-auto grid size-56 place-items-center" aria-hidden="true"><div className="absolute size-56 rounded-full bg-brand-500/30 blur-2xl" /><div className="relative size-36 rounded-full bg-brand-500 shadow-lift" /></div>
      </div>
    </section>
  );
}
