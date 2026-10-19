import { useRef, useState, type FormEvent } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { AuthLayout } from "../components/auth/AuthLayout";
import { CaptchaWidget, type CaptchaHandle } from "../components/auth/CaptchaWidget";
import { GoogleButton } from "../components/auth/GoogleButton";
import { PasswordField } from "../components/auth/PasswordField";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import { HCAPTCHA_SITE_KEY, friendlyAuthError } from "../lib/auth";
import { getStoredRole, roleLabel } from "../lib/role";
import { supabase } from "../lib/supabase";

type LocationState = { from?: string; notice?: string } | null;

export default function LoginPage() {
  const navigate = useNavigate();
  const state = useLocation().state as LocationState;
  const captcha = useRef<CaptchaHandle>(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const stored = getStoredRole();
  if (!stored) return <Navigate to="/role?next=/login" replace />;

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    if (HCAPTCHA_SITE_KEY && !token) {
      setError("Please complete the captcha.");
      return;
    }
    setLoading(true);
    const { error } = await supabase.auth.signInWithPassword({
      email: email.trim(),
      password,
      options: { captchaToken: token ?? undefined },
    });
    setLoading(false);
    if (error) {
      setError(friendlyAuthError(error.message));
      captcha.current?.reset();
      setToken(null);
      return;
    }
    navigate(state?.from ?? "/app", { replace: true });
  }

  return (
    <AuthLayout
      title="Welcome back"
      subtitle="Sign in to get guided help and see your past emergencies."
      footer={<>New here? <Link to="/signup" className="font-semibold text-brand-600 hover:underline">Create an account</Link></>}
    >
      {state?.notice && (
        <p className="mb-5 rounded-xl bg-brand-50 px-3.5 py-2.5 text-sm text-brand-700" role="status">{state.notice}</p>
      )}
      <p className="mb-4 text-xs text-ink-500">Using as: <span className="font-semibold text-ink-700">{roleLabel(stored.role)}</span> · <Link to="/role?next=/login" className="font-semibold text-brand-600">change</Link></p>
      <GoogleButton label="Log in with Google" />
      <div className="my-5 flex items-center gap-3 text-xs text-ink-500">
        <span className="h-px flex-1 bg-ink-200" /> or with email <span className="h-px flex-1 bg-ink-200" />
      </div>
      <form onSubmit={onSubmit} className="space-y-4" noValidate>
        <Input label="Email" type="email" autoComplete="email" required value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
        <PasswordField autoComplete="current-password" required value={password} onChange={(e) => setPassword(e.target.value)} />
        <div className="text-right">
          <Link to="/forgot-password" className="text-sm font-medium text-brand-600 hover:underline">Forgot password?</Link>
        </div>
        <CaptchaWidget ref={captcha} onToken={setToken} />
        {error && <p className="rounded-xl bg-emergency-50 px-3.5 py-2.5 text-sm text-emergency-600" role="alert">{error}</p>}
        <Button type="submit" fullWidth loading={loading}>Log in</Button>
      </form>
    </AuthLayout>
  );
}
