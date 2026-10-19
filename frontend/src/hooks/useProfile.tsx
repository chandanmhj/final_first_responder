import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { api } from "../lib/api";
import { getStoredRole } from "../lib/role";
import type { Profile } from "../types/chat";
import { useAuth } from "./useAuth";

type ProfileState = { profile: Profile | null; loading: boolean; needsRole: boolean; error: string | null; refresh: () => Promise<void> };

const Ctx = createContext<ProfileState | null>(null);

/** Loads the profile after login and saves the role chosen before login. */
export function ProfileProvider({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      let p = await api.getMe();
      const stored = getStoredRole();
      if (stored && p.role !== stored.role && (stored.role === "common" || stored.attested)) {
        p = await api.putMe({
          role: stored.role,
          attested: stored.role === "responder" ? true : undefined,
          cert_number: stored.cert || undefined,
          full_name: p.full_name ?? ((user?.user_metadata?.full_name as string | undefined) || undefined),
        });
      }
      setProfile(p);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not load your profile.");
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const value = useMemo(() => ({ profile, loading, needsRole: !loading && !error && !!profile && !profile.role, error, refresh }), [profile, loading, error, refresh]);
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useProfile(): ProfileState {
  const v = useContext(Ctx);
  if (!v) throw new Error("useProfile must be used inside ProfileProvider");
  return v;
}
