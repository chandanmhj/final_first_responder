import { useEffect, useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthLayout } from "../components/auth/AuthLayout";
import { PasswordField } from "../components/auth/PasswordField";
import { Button } from "../components/ui/Button";
import { friendlyAuthError, passwordProblems } from "../lib/auth";
import { supabase } from "../lib/supabase";

type Status = "checking" | "ready" | "invalid";

export default function ResetPasswordPage() {
  const navigate = useNavigate();
  const [status, setStatus] = useState<Status>("checking");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // The emailed link signs the user in temporarily. Wait for that, and give up after a few seconds.
  useEffect(() => {
    const { data } = supabase.auth.onAuthStateChange((event) => {
      if (event === "PASSWORD_RECOVERY") setStatus("ready");
    });
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (session) setStatus((s) => (s === "checking" ? "ready" : s));
    });
    const timer = setTimeout(() => setStatus((s) => (s === "checking" ? "invalid" : s)), 4000);
    return () => {
      data.subscription.unsubscribe();
      clearTimeout(timer);
    };
  }, []);

  const problems = password ? passwordProblems(password) : [];

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    if (passwordProblems(password).length) return setError("Please choose a stronger password.");
    if (password !== confirm) return setError("The passwords don't match.");
    setLoading(true);
    const { error } = await supabase.auth.updateUser({ password });
    if (error) {
      setLoading(false);
      return setError(friendlyAuthError(error.message));
    }
    await supabase.auth.signOut();
    navigate("/login", { replace: true, state: { notice: "Password updated. Please log in with your new password." } });
  }

  return (
    <AuthLayout title="Set a new password" subtitle="Choose a password you haven't used before.">
      {status === "checking" && <p className="text-center text-sm text-ink-500" role="status">Checking your link...</p>}
      {status === "invalid" && (
        <div className="space-y-4 text-center" role="alert">
          <p className="font-display text-lg font-semibold text-ink-950">This link has expired</p>
          <p className="text-sm text-ink-500">Reset links work once and expire after a while. Request a new one.</p>
          <Link to="/forgot-password" className="inline-block font-semibold text-brand-600 hover:underline">Request a new link</Link>
        </div>
      )}
      {status === "ready" && (
        <form onSubmit={onSubmit} className="space-y-4" noValidate>
          <PasswordField
            label="New password"
            autoComplete="new-password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            hint="At least 8 characters, with a letter and a number."
            error={problems.length ? `Needs ${problems.join(", ")}.` : undefined}
          />
          <PasswordField
            label="Confirm new password"
            autoComplete="new-password"
            required
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            error={confirm.length > 0 && confirm !== password ? "The passwords don't match." : undefined}
          />
          {error && <p className="rounded-xl bg-emergency-50 px-3.5 py-2.5 text-sm text-emergency-600" role="alert">{error}</p>}
          <Button type="submit" fullWidth loading={loading}>Update password</Button>
        </form>
      )}
    </AuthLayout>
  );
}
