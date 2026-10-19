import type { ScenarioInfo } from "../../types/chat";

/** Thin header strip: which emergency, and how far along. */
export function StepTimeline({ scenario }: { scenario: ScenarioInfo | null }) {
  if (!scenario || scenario.total === 0) return null;
  const done = scenario.status === "completed" ? scenario.total : scenario.index;
  return (
    <div className="flex items-center gap-3 text-xs text-ink-500">
      <span className="truncate font-semibold text-ink-700">{scenario.title}</span>
      <span className="shrink-0">{done}/{scenario.total} done</span>
      <div className="hidden h-1.5 w-28 overflow-hidden rounded-full bg-ink-100 sm:block">
        <div className="h-full rounded-full bg-success-500 transition-all" style={{ width: `${(done / scenario.total) * 100}%` }} />
      </div>
    </div>
  );
}
