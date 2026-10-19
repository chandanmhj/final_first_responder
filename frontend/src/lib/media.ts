import type { StepMedia } from "../types/chat";

const warmed = new Set<string>();

/** Start loading the next step's media so it appears instantly when the user taps Next. */
export function prefetchMedia(m: StepMedia | null | undefined): void {
  if (!m) return;
  if (m.image && !warmed.has(m.image)) {
    warmed.add(m.image);
    const img = new Image();
    img.decoding = "async";
    img.src = m.image;
  }
  if (m.video && !warmed.has(m.video)) {
    warmed.add(m.video);
    const v = document.createElement("video");
    v.preload = "auto";
    v.muted = true;
    v.src = m.video;
  }
}
