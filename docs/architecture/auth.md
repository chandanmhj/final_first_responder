# Authentication

Status: provider and pages **Decided**; details **Proposed**.

Auth runs on Supabase Auth. **Login is required for everything** (no guest access, Decided), because the responses depend on
the user's role. The backend verifies the access token on every protected route.

## Pages
- Sign up (email + password, Continue with Google, hCaptcha)
- Login (same options)
- Forgot password (same neutral message whether or not the account exists)
- Reset password (from the emailed link, with expired-link state)
- Verify email (check-your-inbox screen with resend)
- Auth callback (OAuth return)
- Profile (name, role preference, change password, delete account)

Every page needs loading and error states, keyboard and screen-reader support, and a mobile layout.

## Setup notes
- Google: create OAuth credentials in Google Cloud and add Supabase's callback URL.
- hCaptcha: enable it in Supabase Auth settings with the hCaptcha secret; the frontend uses the site key.
- Set the Supabase site URL and redirect allow-list for localhost and the Netlify domain.
- Use custom SMTP for emails; the default Supabase sender has low rate limits.
- Menu names in dashboards change, so check the current Supabase docs when configuring.

## Note
Requiring login before help can slow someone down in a real emergency. Decided by you; recorded here so it can be revisited.
