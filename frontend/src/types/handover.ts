export type { HandoverReport } from "./chat";
export type IncidentSummary = { id: string; title: string; started_at: string; status: string | null };
export type HandoverResponse = { report: import("./chat").HandoverReport; markdown: string };
