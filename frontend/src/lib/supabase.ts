import { createClient } from "@supabase/supabase-js";

const url = import.meta.env.VITE_SUPABASE_URL;
const anonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

/** True when both Supabase environment variables are present. */
export const isSupabaseConfigured = Boolean(url && anonKey);

/**
 * Shared Supabase client. Only the public anon key is used in the browser.
 * PKCE is used so email links and Google sign-in return a one-time code.
 */
export const supabase = createClient(url ?? "http://localhost:54321", anonKey ?? "missing-anon-key", {
  auth: {
    flowType: "pkce",
    persistSession: true,
    autoRefreshToken: true,
    detectSessionInUrl: true,
  },
});
