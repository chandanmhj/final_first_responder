import { useRef, useState, type FormEvent } from "react";
import { Link } from "react-router-dom";
import { AuthLayout } from "../components/auth/AuthLayout";
import { CaptchaWidget, type CaptchaHandle } from "../components/auth/CaptchaWidget";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import { HCAPTCHA_SITE_KEY, appUrl, friendlyAuthError } from "../lib/auth";
import { supabase } from "../lib/supabase";

export default function ForgotPasswordPage() {
  const captcha = useRef<CaptchaHandle>(null);
  const [email, setEmail] = useState("");
  const [token, setToken] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    if (HCAPTCHA_SITE_KEY && !token) return setError("Please complete the captcha.");
    setLoading(true);
    const { error } = await supabase.auth.resetPasswordForEmail(email.trim(), {
      redirectTo: appUrl("/reset-password"),
      captchaToken: token ?? undefined,
    });
    setLoading(false);
    // Same message whether or not the account exists, so nobody can probe which emails are registered.
    if (error && !error.message.toLowerCase().includes("not found")) {
      setError(friendlyAuthError(error.message));
      captcha.current?.reset();
      setToken(null);
      return;
    }
    setSent(true);
  }

  return (
    <AuthLayout
      title="Forgot your password?"
      subtitle="Enter your email and we'll send you a link to set a new one."
      footer={<Link to="/login" className="font-semibold text-brand-600 hover:underline">Back to log in</Link>}
    >
      {sent ? (
        <div className="space-y-3 text-center" role="status">
          <p className="font-display text-lg font-semibold text-ink-950">Check your inbox</p>
          <p className="text-sm text-ink-500">
            If an account exists for <span className="font-medium text-ink-700">{email}</span>, a reset link is on its way. It may take a minute.
          </p>
        </div>
      ) : (
        <form onSubmit={onSubmit} className="space-y-4" noValidate>
          <Input label="Email" type="email" autoComplete="email" required value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
          <CaptchaWidget ref={captcha} onToken={setToken} />
          {error && <p className="rounded-xl bg-emergency-50 px-3.5 py-2.5 text-sm text-emergency-600" role="alert">{error}</p>}
          <Button type="submit" fullWidth loading={loading}>Send reset link</Button>
        </form>
      )}
    </AuthLayout>
  );
}
