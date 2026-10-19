import { useEffect, useRef, useState } from "react";
import { Link, Navigate, useLocation } from "react-router-dom";
import { AuthLayout } from "../components/auth/AuthLayout";
import { CaptchaWidget, type CaptchaHandle } from "../components/auth/CaptchaWidget";
import { Button } from "../components/ui/Button";
import { HCAPTCHA_SITE_KEY, appUrl, friendlyAuthError } from "../lib/auth";
import { supabase } from "../lib/supabase";

const COOLDOWN_SECONDS = 60;

export default function VerifyEmailPage() {
  const email = (useLocation().state as { email?: string } | null)?.email;
  const captcha = useRef<CaptchaHandle>(null);
  const [token, setToken] = useState<string | null>(null);
  const [cooldown, setCooldown] = useState(0);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (cooldown <= 0) return;
    const t = setTimeout(() => setCooldown((c) => c - 1), 1000);
    return () => clearTimeout(t);
  }, [cooldown]);

  if (!email) return <Navigate to="/signup" replace />;

  async function resend() {
    setError(null);
    setMessage(null);
    if (HCAPTCHA_SITE_KEY && !token) return setError("Please complete the captcha to resend.");
    setLoading(true);
    const { error } = await supabase.auth.resend({
      type: "signup",
      email: email as string,
      options: { emailRedirectTo: appUrl("/auth/callback"), captchaToken: token ?? undefined },
    });
    setLoading(false);
    captcha.current?.reset();
    setToken(null);
    if (error) return setError(friendlyAuthError(error.message));
    setMessage("We sent another email.");
    setCooldown(COOLDOWN_SECONDS);
  }

  return (
    <AuthLayout
      title="Check your inbox"
      subtitle={`We sent a confirmation link to ${email}. Open it to finish creating your account.`}
      footer={<Link to="/login" className="font-semibold text-brand-600 hover:underline">Back to log in</Link>}
    >
      <div className="space-y-4">
        <p className="text-sm text-ink-500">Can't find it? Check your spam folder, or send it again.</p>
        <CaptchaWidget ref={captcha} onToken={setToken} />
        {message && <p className="rounded-xl bg-brand-50 px-3.5 py-2.5 text-sm text-brand-700" role="status">{message}</p>}
        {error && <p className="rounded-xl bg-emergency-50 px-3.5 py-2.5 text-sm text-emergency-600" role="alert">{error}</p>}
        <Button type="button" variant="secondary" fullWidth loading={loading} disabled={cooldown > 0} onClick={resend}>
          {cooldown > 0 ? `Send again in ${cooldown}s` : "Send the email again"}
        </Button>
      </div>
    </AuthLayout>
  );
}
