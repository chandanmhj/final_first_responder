import type { Citation } from "../../types/chat";

/** Where an answer comes from. */
export function CitationList({ citations }: { citations?: Citation[] }) {
  if (!citations?.length) return null;
  return (
    <details className="mt-2 text-xs text-ink-500">
      <summary className="cursor-pointer select-none font-medium text-ink-700">Sources ({citations.length})</summary>
      <ul className="mt-1.5 space-y-1">
        {citations.map((c) => (
          <li key={`${c.source}-${c.topic}-${c.page}`} className="leading-snug">
            {c.label} <span className="text-ink-300">· {c.topic}</span>
          </li>
        ))}
      </ul>
    </details>
  );
}
