import { useEffect } from "react";
import { prefetchMedia } from "../lib/media";
import type { StepMedia } from "../types/chat";

/** Warm the cache for the next step's media while the user reads the current step. */
export function useMediaPrefetch(next: StepMedia | null | undefined): void {
  useEffect(() => {
    prefetchMedia(next);
  }, [next]);
}
