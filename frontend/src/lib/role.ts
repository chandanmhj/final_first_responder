import type { Role } from "../types/chat";

const KEY = "fr_role";

export type StoredRole = { role: Role; attested: boolean; cert: string };

/** Role chosen before login. Kept in the browser, then saved to the profile after login. */
export function getStoredRole(): StoredRole | null {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return null;
    const v = JSON.parse(raw) as StoredRole;
    return v.role === "common" || v.role === "responder" ? v : null;
  } catch {
    return null;
  }
}

export function setStoredRole(v: StoredRole): void {
  try {
    localStorage.setItem(KEY, JSON.stringify(v));
  } catch {
    /* storage unavailable: the profile still holds the role after login */
  }
}

export function roleLabel(role: Role | null | undefined): string {
  return role === "responder" ? "Certified first responder" : "Common person";
}
