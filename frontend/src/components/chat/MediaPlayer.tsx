import { useState } from "react";
import type { StepMedia } from "../../types/chat";

/** Short looping clip or image for a step. Renders nothing when the step has no media (text only). */
export function MediaPlayer({ media, title }: { media: StepMedia; title: string }) {
  const [tab, setTab] = useState<"video" | "image">(media.video ? "video" : "image");
  const [failed, setFailed] = useState(false);
  if ((!media.video && !media.image) || failed) return null;
  const both = media.video && media.image;
  return (
    <div className="mt-4 overflow-hidden rounded-2xl border border-ink-100 bg-ink-50">
      {tab === "video" && media.video ? (
        <video
          src={media.video}
          className="aspect-video w-full bg-ink-950 object-contain"
          controls
          muted
          loop
          playsInline
          preload="metadata"
          aria-label={`Video: ${title}`}
          onError={() => setFailed(true)}
        />
      ) : (
        media.image && <img src={media.image} alt={title} loading="lazy" decoding="async" className="aspect-video w-full object-contain" onError={() => setFailed(true)} />
      )}
      {both && (
        <div className="flex gap-1 border-t border-ink-100 p-1.5">
          {(["video", "image"] as const).map((t) => (
            <button key={t} type="button" onClick={() => setTab(t)} className={`flex-1 rounded-lg py-1.5 text-xs font-semibold ${tab === t ? "bg-white text-brand-700 shadow-soft" : "text-ink-500"}`}>
              {t === "video" ? "Watch" : "Picture"}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
