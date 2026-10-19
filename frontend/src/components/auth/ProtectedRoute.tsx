import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import { ProfileProvider } from "../../hooks/useProfile";

function FullScreenSpinner() {
  return (
    <div className="grid min-h-dvh place-items-center">
      <svg className="size-8 animate-spin text-brand-600" viewBox="0 0 24 24" fill="none" aria-label="Loading">
        <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" opacity="0.25" />
        <path d="M22 12a10 10 0 0 0-10-10" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
      </svg>
    </div>
  );
}

/** Only signed-in users may see the nested routes. The profile (role) loads once for all of them. */
export function ProtectedRoute() {
  const { user, loading } = useAuth();
  const location = useLocation();
  if (loading) return <FullScreenSpinner />;
  if (!user) return <Navigate to="/role?next=/login" replace state={{ from: location.pathname }} />;
  return <ProfileProvider><Outlet /></ProfileProvider>;
}

/** Signed-in users are sent to the app. Everyone else must have picked a role first. */
export function PublicOnlyRoute() {
  const { user, loading } = useAuth();
  if (loading) return <FullScreenSpinner />;
  if (user) return <Navigate to="/app" replace />;
  return <Outlet />;
}
