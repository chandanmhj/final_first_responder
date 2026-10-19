/** Public hCaptcha site key. Empty in development when captcha is turned off in Supabase. */
export const HCAPTCHA_SITE_KEY = import.meta.env.VITE_HCAPTCHA_SITE_KEY;

/** Build an absolute URL on this site, used for email and OAuth redirects. */
export function appUrl(path: string): string {
  return `${window.location.origin}${path}`;
}

/** Turn a Supabase auth error message into something a person can act on. */
export function friendlyAuthError(message: string): string {
  const m = message.toLowerCase();
  if (m.includes("invalid login credentials")) return "That email and password don't match. Check them and try again.";
  if (m.includes("email not confirmed")) return "Please confirm your email first. Check your inbox for the link.";
  if (m.includes("already registered") || m.includes("already been registered")) return "An account with this email already exists. Try signing in.";
  if (m.includes("captcha")) return "The captcha check failed. Please try the captcha again.";
  if (m.includes("rate limit") || m.includes("too many")) return "Too many attempts. Please wait a minute and try again.";
  if (m.includes("password should be")) return "That password is too weak. Use at least 8 characters with a letter and a number.";
  if (m.includes("network") || m.includes("failed to fetch")) return "Can't reach the server. Check your connection and try again.";
  return "Something went wrong. Please try again.";
}

/** Return the list of rules a password breaks. An empty list means the password is acceptable. */
export function passwordProblems(password: string): string[] {
  const problems: string[] = [];
  if (password.length < 8) problems.push("at least 8 characters");
  if (!/[A-Za-z]/.test(password)) problems.push("a letter");
  if (!/[0-9]/.test(password)) problems.push("a number");
  return problems;
}
