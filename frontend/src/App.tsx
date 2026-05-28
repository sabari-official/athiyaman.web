import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "sonner";
import { AuthProvider, useAuth } from "./lib/auth";

// Authenticated Pages
import { Login } from "./pages/Login";
import { ChangePassword } from "./pages/ChangePassword";
import { ApplyLeader } from "./pages/ApplyLeader";
import { ApplyMember } from "./pages/ApplyMember";
import { Signup } from "./pages/Signup";
import { ProfileGuard } from "./components/athi/ProfileGuard";
import { Instructions } from "./pages/Instructions";
import { DashboardLayout } from "./pages/DashboardLayout";
import { DashboardIndex } from "./pages/DashboardIndex";
import { WasteHistory } from "./pages/WasteHistory";
import { ClaimsHistory } from "./pages/ClaimsHistory";
import { NotificationsCenter } from "./pages/NotificationsCenter";
import { TeamRoster } from "./pages/TeamRoster";
import { ReferralCodes } from "./pages/ReferralCodes";
import { AdminHome } from "./pages/AdminHome";
import { DeveloperHome } from "./pages/DeveloperHome";

// Public Website Pages
import { PublicHome } from "./pages/public/Home";
import { PublicAbout } from "./pages/public/About";
import { PublicHowItWorks } from "./pages/public/HowItWorks";
import { PublicPlans } from "./pages/public/Plans";
import { PublicGallery } from "./pages/public/Gallery";
import { PublicContact } from "./pages/public/Contact";

// Initialize Query Client for API state caching
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function RouteGuard({ children, allowedRoles }: { children: React.ReactNode; allowedRoles?: string[] }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background text-muted-foreground text-sm font-medium">
        Loading Auth Session…
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
}

function MainRoutes() {
  return (
    <Routes>
      {/* Public Landing Website */}
      <Route path="/" element={<PublicHome />} />
      <Route path="/about" element={<PublicAbout />} />
      <Route path="/how-it-works" element={<PublicHowItWorks />} />
      <Route path="/plans" element={<PublicPlans />} />
      <Route path="/gallery" element={<PublicGallery />} />
      <Route path="/contact" element={<PublicContact />} />

      {/* Authentication Routes */}
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/apply-leader" element={<ApplyLeader />} />
      <Route path="/join-member" element={<ApplyMember />} />
      
      {/* Protected - Instructions Page (Available after login) */}
      <Route
        path="/instructions"
        element={
          <RouteGuard>
            <Instructions />
          </RouteGuard>
        }
      />

      {/* Protected - Password Change */}
      <Route
        path="/change-password"
        element={
          <RouteGuard>
            <ChangePassword />
          </RouteGuard>
        }
      />

      {/* Protected Dashboard (Placeholder - integrate your existing dashboard) */}
      <Route
        path="/dashboard"
        element={
          <RouteGuard allowedRoles={["MEMBER", "LEADER"]}>
            <ProfileGuard>
              <DashboardLayout />
            </ProfileGuard>
          </RouteGuard>
        }
      >
        <Route index element={<DashboardIndex />} />
        <Route path="waste" element={<WasteHistory />} />
        <Route path="payments" element={<ClaimsHistory />} />
        <Route path="notifications" element={<NotificationsCenter />} />
        <Route path="team" element={<TeamRoster />} />
        <Route path="referrals" element={<ReferralCodes />} />
      </Route>

      {/* Protected Admin + Developer panels (minimal placeholders) */}
      <Route
        path="/admin"
        element={
          <RouteGuard allowedRoles={["ADMIN"]}>
            <AdminHome />
          </RouteGuard>
        }
      />
      <Route
        path="/developer"
        element={
          <RouteGuard allowedRoles={["DEVELOPER"]}>
            <DeveloperHome />
          </RouteGuard>
        }
      />

      {/* Fallback Redirections */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <MainRoutes />
          <Toaster position="top-right" richColors />
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
