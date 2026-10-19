import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthLayout } from "../components/auth/AuthLayout";
import { useAuth } from "../hooks/useAuth";

/** Where email confirmation links and Google sign-in return to. */
export default function AuthCallbackPage() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();
  const [timedOut, setTimedOut] = useState(false);

  const params = new URLSearchParams(window.location.search);
  const hash = new URLSearchParams(window.location.hash.replace(/^#/, ""));
  const urlError = params.get("error_description") ?? hash.get("error_description");

  useEffect(() => {
    if (!loading && user) navigate("/app", { replace: true });
  }, [loading, user, navigate]);

  useEffect(() => {
    const t = setTimeout(() => setTimedOut(true), 8000);
    return () => clearTimeout(t);
  }, []);

  const failed = Boolean(urlError) || (timedOut && !user);

  return (
    <AuthLayout title={failed ? "We couldn't sign you in" : "Signing you in..."}>
      {failed ? (
        <div className="space-y-4 text-center" role="alert">
          <p className="text-sm text-ink-500">{urlError ?? "The link may have expired or was already used."}</p>
          <Link to="/login" className="inline-block font-semibold text-brand-600 hover:underline">Back to log in</Link>
        </div>
      ) : (
        <p className="text-center text-sm text-ink-500" role="status">One moment while we finish signing you in.</p>
      )}
    </AuthLayout>
  );
}
