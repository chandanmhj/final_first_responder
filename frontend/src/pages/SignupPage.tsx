import { useRef, useState, type FormEvent } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { AuthLayout } from "../components/auth/AuthLayout";
import { CaptchaWidget, type CaptchaHandle } from "../components/auth/CaptchaWidget";
import { GoogleButton } from "../components/auth/GoogleButton";
import { PasswordField } from "../components/auth/PasswordField";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import { HCAPTCHA_SITE_KEY, appUrl, friendlyAuthError, passwordProblems } from "../lib/auth";
import { getStoredRole, roleLabel } from "../lib/role";
import { supabase } from "../lib/supabase";

export default function SignupPage() {
  const navigate = useNavigate();
  const captcha = useRef<CaptchaHandle>(null);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [token, setToken] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const problems = password ? passwordProblems(password) : [];
  const mismatch = confirm.length > 0 && confirm !== password;

  const stored = getStoredRole();
  if (!stored) return <Navigate to="/role?next=/signup" replace />;

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    if (!name.trim()) return setError("Please enter your name.");
    if (passwordProblems(password).length) return setError("Please choose a stronger password.");
    if (password !== confirm) return setError("The passwords don't match.");
    if (HCAPTCHA_SITE_KEY && !token) return setError("Please complete the captcha.");

    setLoading(true);
    const { data, error } = await supabase.auth.signUp({
      email: email.trim(),
      password,
      options: {
        data: { full_name: name.trim() },
        emailRedirectTo: appUrl("/auth/callback"),
        captchaToken: token ?? undefined,
      },
    });
    setLoading(false);
    if (error) {
      setError(friendlyAuthError(error.message));
      captcha.current?.reset();
      setToken(null);
      return;
    }
    if (data.session) navigate("/app", { replace: true });
    else navigate("/verify-email", { replace: true, state: { email: email.trim() } });
  }

  return (
    <AuthLayout
      title="Create your account"
      subtitle="It takes a minute. Your account keeps your emergencies and reports safe."
      footer={<>Already have an account? <Link to="/login" className="font-semibold text-brand-600 hover:underline">Log in</Link></>}
    >
      <p className="mb-4 text-xs text-ink-500">Using as: <span className="font-semibold text-ink-700">{roleLabel(stored.role)}</span> · <Link to="/role?next=/signup" className="font-semibold text-brand-600">change</Link></p>
      <GoogleButton label="Sign up with Google" />
      <div className="my-5 flex items-center gap-3 text-xs text-ink-500">
        <span className="h-px flex-1 bg-ink-200" /> or with email <span className="h-px flex-1 bg-ink-200" />
      </div>
      <form onSubmit={onSubmit} className="space-y-4" noValidate>
        <Input label="Full name" autoComplete="name" required value={name} onChange={(e) => setName(e.target.value)} />
        <Input label="Email" type="email" autoComplete="email" required value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
        <PasswordField
          autoComplete="new-password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          hint="At least 8 characters, with a letter and a number."
          error={problems.length ? `Needs ${problems.join(", ")}.` : undefined}
        />
        <PasswordField
          label="Confirm password"
          autoComplete="new-password"
          required
          value={confirm}
          onChange={(e) => setConfirm(e.target.value)}
          error={mismatch ? "The passwords don't match." : undefined}
        />
        <CaptchaWidget ref={captcha} onToken={setToken} />
        {error && <p className="rounded-xl bg-emergency-50 px-3.5 py-2.5 text-sm text-emergency-600" role="alert">{error}</p>}
        <Button type="submit" fullWidth loading={loading}>Create account</Button>
      </form>
    </AuthLayout>
  );
}
