const faqs = [
  ["Is this a replacement for an ambulance?", "No. Call 108 first in any emergency. This app guides you while help is on the way."],
  ["Who is it for?", "Anyone. Common people get simple words. Certified first responders get clinical wording and responder-level steps."],
  ["Can I trust the photo result?", "Treat it as a best guess with a confidence level. You are always told to visit a hospital after a bite or sting."],
  ["Are my chats saved?", "Yes, your conversations and handover reports are stored in your account so you can open them later."],
  ["Which guidelines does it use?", "See the Sources page. Steps show where they come from."],
];

export function Faq() {
  return (
    <section id="faq" className="mx-auto max-w-3xl px-5 py-20">
      <h2 className="text-3xl font-bold text-ink-950">Questions</h2>
      <div className="mt-8 divide-y divide-ink-100 rounded-2xl border border-ink-100 bg-white shadow-soft">
        {faqs.map(([q, a]) => <details key={q} className="group p-5"><summary className="cursor-pointer list-none font-semibold text-ink-950">{q}</summary><p className="mt-2 text-sm text-ink-500">{a}</p></details>)}
      </div>
    </section>
  );
}
