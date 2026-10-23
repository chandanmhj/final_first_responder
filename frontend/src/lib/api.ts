import { supabase } from "./supabase";
import type { ChatResponse, Hospital, Profile, Role, SessionSummary } from "../types/chat";
import type { ConditionOption } from "../types/scenario";
import type { HandoverResponse, IncidentSummary } from "../types/handover";

const BASE = (import.meta.env.VITE_API_BASE_URL ?? "").replace(/\/$/, "");

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function authHeader(): Promise<Record<string, string>> {
  const { data } = await supabase.auth.getSession();
  const token = data.session?.access_token;
  return token ? { Authorization: `Bearer ${token}` } : {};
}

/** Call the backend with the user's access token. Throws ApiError with a readable message. */
export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${BASE}${path}`, { ...init, headers: { ...(await authHeader()), ...(init.headers ?? {}) } });
  } catch {
    throw new ApiError("Can't reach the server. It may be waking up. Please try again in a moment.", 0);
  }
  if (!res.ok) {
    let msg = "Something went wrong. Please try again.";
    try {
      const j = (await res.json()) as { message?: string; detail?: unknown };
      if (j.message) msg = j.message;
      else if (typeof j.detail === "string") msg = j.detail;
    } catch {
      /* keep default message */
    }
    throw new ApiError(msg, res.status);
  }
  return (await res.json()) as T;
}

const json = (body: unknown): RequestInit => ({ method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });

export const api = {
  health: () => apiFetch<{ status: string }>("/health"),
  getMe: () => apiFetch<Profile>("/api/me"),
  putMe: (body: { full_name?: string; role?: Role; cert_number?: string; attested?: boolean; age?: number; sex?: string; blood_group?: string; allergies?: string; conditions?: string; medications?: string; emergency_contact?: string }) =>
    apiFetch<Profile>("/api/me", { ...json(body), method: "PUT" }),
  listSessions: () => apiFetch<SessionSummary[]>("/api/sessions"),
  getMessages: (id: string) =>
    apiFetch<{ session: { id: string; title: string; state: Record<string, unknown> }; messages: { id: string; role: "user" | "assistant"; content: Record<string, unknown>; created_at: string }[] }>(
      `/api/sessions/${id}/messages`,
    ),
  deleteSession: (id: string) => apiFetch<{ ok: boolean }>(`/api/sessions/${id}`, { method: "DELETE" }),
  renameSession: (id: string, title: string) => apiFetch<{ ok: boolean }>(`/api/sessions/${id}`, { ...json({ title }), method: "PATCH" }),
  pinSession: (id: string, pinned: boolean) => apiFetch<{ ok: boolean }>(`/api/sessions/${id}`, { ...json({ pinned }), method: "PATCH" }),
  chat: (form: FormData) => apiFetch<ChatResponse>("/api/chat", { method: "POST", body: form }),
  transcribe: (wav: Blob) => {
    const f = new FormData();
    f.append("audio", wav, "speech.wav");
    return apiFetch<{ text: string }>("/api/voice/transcribe", { method: "POST", body: f });
  },
  hospitals: (lat: number, lon: number, condition?: string) =>
    apiFetch<{ results: Hospital[]; message: string | null }>(
      `/api/hospitals/nearby?lat=${lat}&lon=${lon}${condition ? `&condition=${encodeURIComponent(condition)}` : ""}`,
    ),
  conditions: () => apiFetch<ConditionOption[]>("/api/scenarios/conditions"),
  incidents: () => apiFetch<IncidentSummary[]>("/api/incidents"),
  handover: (id: string) => apiFetch<HandoverResponse>(`/api/incidents/${id}/handover`),
  addEvent: (id: string, event_type: string, text?: string) => apiFetch<{ id: string }>(`/api/incidents/${id}/events`, json({ event_type, text })),
};

/** Ask the browser for the user's position. Resolves null if denied or unavailable. */
export function getCoords(timeoutMs = 8000): Promise<{ lat: number; lon: number } | null> {
  return new Promise((resolve) => {
    if (!navigator.geolocation) return resolve(null);
    navigator.geolocation.getCurrentPosition(
      (p) => resolve({ lat: p.coords.latitude, lon: p.coords.longitude }),
      () => resolve(null),
      { enableHighAccuracy: true, timeout: timeoutMs, maximumAge: 60000 },
    );
  });
}