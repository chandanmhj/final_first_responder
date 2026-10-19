import { AuthProvider } from "./hooks/useAuth";
import { isSupabaseConfigured } from "./lib/supabase";
import { AppRoutes } from "./routes";

function MissingConfig() {
  return (
    <div className="grid min-h-dvh place-items-center px-5">
      <div className="max-w-lg rounded-2xl border border-emergency-500/30 bg-white p-8 shadow-soft">
        <h1 className="text-xl font-bold text-ink-950">Supabase isn't configured</h1>
        <p className="mt-2 text-sm text-ink-500">
          Create <code className="rounded bg-ink-100 px-1.5 py-0.5">frontend/.env</code> with{" "}
          <code className="rounded bg-ink-100 px-1.5 py-0.5">VITE_SUPABASE_URL</code> and{" "}
          <code className="rounded bg-ink-100 px-1.5 py-0.5">VITE_SUPABASE_ANON_KEY</code>, then restart the dev server.
        </p>
      </div>
    </div>
  );
}

export default function App() {
  if (!isSupabaseConfigured) return <MissingConfig />;
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}
