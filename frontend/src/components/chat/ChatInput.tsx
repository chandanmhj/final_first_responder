import { useRef, useState, type FormEvent, type KeyboardEvent } from "react";

export const AGE_BANDS: { id: string; label: string }[] = [
  { id: "0-1", label: "Baby under 1" },
  { id: "1-5", label: "1 to 5" },
  { id: "5-10", label: "5 to 10" },
  { id: "10-18", label: "10 to 18" },
  { id: "18+", label: "Adult" },
];

export type SendOptions = { image?: File | null; forSelf?: boolean; ageBand?: string };

type Props = {
  onSend: (text: string, opts: SendOptions) => void;
  disabled?: boolean;
  /** Show the "for me / someone else" and age choices (before an emergency starts). */
  showContext?: boolean;
  onHandsFree?: () => void;
  handsFreeSupported?: boolean;
  placeholder?: string;
};

/** Text box with photo attach, hands-free button, and the two quick questions asked at the start of an emergency. */
export function ChatInput({ onSend, disabled, showContext, onHandsFree, handsFreeSupported, placeholder = "Describe what happened, or attach a photo" }: Props) {
  const [text, setText] = useState("");
  const [image, setImage] = useState<File | null>(null);
  const [forSelf, setForSelf] = useState<boolean | undefined>(undefined);
  const [age, setAge] = useState<string | undefined>(undefined);
  const file = useRef<HTMLInputElement>(null);

  const submit = (e?: FormEvent) => {
    e?.preventDefault();
    if (disabled || (!text.trim() && !image)) return;
    onSend(text, { image, forSelf, ageBand: age });
    setText("");
    setImage(null);
    if (file.current) file.current.value = "";
  };
  const onKey = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) submit(e);
  };
  const chip = (on: boolean) => `rounded-full border px-3 py-1.5 text-xs font-semibold transition-colors ${on ? "border-brand-600 bg-brand-600 text-white" : "border-ink-200 bg-white text-ink-700 hover:bg-ink-50"}`;

  return (
    <form onSubmit={submit} className="border-t border-ink-100 bg-white/90 px-3 pb-[max(0.75rem,env(safe-area-inset-bottom))] pt-3 backdrop-blur sm:px-6">
      {showContext && (
        <div className="mx-auto mb-3 flex max-w-3xl flex-wrap items-center gap-2">
          <span className="text-xs font-medium text-ink-500">Who needs help?</span>
          <button type="button" className={chip(forSelf === true)} onClick={() => setForSelf(forSelf === true ? undefined : true)}>Me</button>
          <button type="button" className={chip(forSelf === false)} onClick={() => setForSelf(forSelf === false ? undefined : false)}>Someone else</button>
          <span className="ml-2 text-xs font-medium text-ink-500">Age</span>
          {AGE_BANDS.map((b) => (
            <button key={b.id} type="button" className={chip(age === b.id)} onClick={() => setAge(age === b.id ? undefined : b.id)}>{b.label}</button>
          ))}
        </div>
      )}
      {image && (
        <div className="mx-auto mb-2 flex max-w-3xl items-center gap-2 rounded-xl bg-ink-50 px-3 py-2 text-xs text-ink-700">
          <span className="truncate">{image.name}</span>
          <button type="button" onClick={() => { setImage(null); if (file.current) file.current.value = ""; }} className="ml-auto font-semibold text-emergency-600">Remove</button>
        </div>
      )}
      <div className="mx-auto flex max-w-3xl items-end gap-2">
        <input ref={file} type="file" accept="image/jpeg,image/png,image/webp" capture="environment" hidden onChange={(e) => setImage(e.target.files?.[0] ?? null)} />
        <button type="button" onClick={() => file.current?.click()} aria-label="Attach a photo" className="grid size-11 shrink-0 place-items-center rounded-xl border border-ink-200 bg-white text-ink-700 hover:bg-ink-50">
          <svg viewBox="0 0 24 24" className="size-5" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M4 8h3l2-3h6l2 3h3v11H4z" /><circle cx="12" cy="13" r="3.5" /></svg>
        </button>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={onKey}
          rows={1}
          placeholder={placeholder}
          aria-label="Message"
          className="max-h-32 min-h-11 flex-1 resize-none rounded-xl border border-ink-200 bg-white px-3.5 py-2.5 text-sm placeholder:text-ink-300 focus:border-brand-500 focus:outline-none focus:ring-4 focus:ring-brand-100"
        />
        {handsFreeSupported && onHandsFree && (
          <button type="button" onClick={onHandsFree} aria-label="Start hands-free mode" className="grid size-11 shrink-0 place-items-center rounded-xl border border-ink-200 bg-white text-ink-700 hover:bg-ink-50">
            <svg viewBox="0 0 24 24" className="size-5" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M3 12a9 9 0 0 1 18 0" /><rect x="2.5" y="12" width="4" height="7" rx="1.5" /><rect x="17.5" y="12" width="4" height="7" rx="1.5" /></svg>
          </button>
        )}
        <button type="submit" disabled={disabled || (!text.trim() && !image)} aria-label="Send" className="grid size-11 shrink-0 place-items-center rounded-xl bg-brand-600 text-white shadow-soft hover:bg-brand-700 disabled:opacity-50">
          <svg viewBox="0 0 24 24" className="size-5" fill="currentColor" aria-hidden="true"><path d="M3.4 20.4 21 12 3.4 3.6 3.3 10l12 2-12 2z" /></svg>
        </button>
      </div>
    </form>
  );
}
