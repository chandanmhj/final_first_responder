import HCaptcha from "@hcaptcha/react-hcaptcha";
import { forwardRef, useImperativeHandle, useRef } from "react";
import { HCAPTCHA_SITE_KEY } from "../../lib/auth";

export type CaptchaHandle = { reset: () => void };

type Props = { onToken: (token: string | null) => void };

/**
 * hCaptcha widget. When no site key is configured (local development with captcha
 * switched off in Supabase) it renders nothing and the form submits without a token.
 */
export const CaptchaWidget = forwardRef<CaptchaHandle, Props>(function CaptchaWidget({ onToken }, ref) {
  const inner = useRef<HCaptcha>(null);

  useImperativeHandle(ref, () => ({
    reset: () => inner.current?.resetCaptcha(),
  }));

  if (!HCAPTCHA_SITE_KEY) return null;

  return (
    <div className="flex justify-center">
      <HCaptcha
        ref={inner}
        sitekey={HCAPTCHA_SITE_KEY}
        onVerify={(token) => onToken(token)}
        onExpire={() => onToken(null)}
        onError={() => onToken(null)}
      />
    </div>
  );
});
