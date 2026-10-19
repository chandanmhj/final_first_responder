import { Route, Routes } from "react-router-dom";
import { AppShell } from "./components/chat/AppShell";
import { ProtectedRoute, PublicOnlyRoute } from "./components/auth/ProtectedRoute";
import AboutPage from "./pages/AboutPage";
import AuthCallbackPage from "./pages/AuthCallbackPage";
import ChatPage from "./pages/ChatPage";
import ConversationsPage from "./pages/ConversationsPage";
import ForgotPasswordPage from "./pages/ForgotPasswordPage";
import HandoverReportPage from "./pages/HandoverReportPage";
import HospitalsPage from "./pages/HospitalsPage";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import NotFoundPage from "./pages/NotFoundPage";
import ProfilePage from "./pages/ProfilePage";
import ReportsPage from "./pages/ReportsPage";
import ResetPasswordPage from "./pages/ResetPasswordPage";
import RolePage from "./pages/RolePage";
import SignupPage from "./pages/SignupPage";
import VerifyEmailPage from "./pages/VerifyEmailPage";

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/about" element={<AboutPage />} />
      <Route path="/role" element={<RolePage />} />
      <Route element={<PublicOnlyRoute />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/verify-email" element={<VerifyEmailPage />} />
      </Route>
      <Route path="/reset-password" element={<ResetPasswordPage />} />
      <Route path="/auth/callback" element={<AuthCallbackPage />} />
      <Route element={<ProtectedRoute />}>
        <Route element={<AppShell />}>
          <Route path="/app" element={<ConversationsPage />} />
          <Route path="/app/c/:id" element={<ChatPage />} />
          <Route path="/app/hospitals" element={<HospitalsPage />} />
          <Route path="/app/reports" element={<ReportsPage />} />
          <Route path="/app/incident/:id/report" element={<HandoverReportPage />} />
          <Route path="/app/profile" element={<ProfilePage />} />
        </Route>
      </Route>
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
