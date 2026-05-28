import { useEffect } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../lib/auth";
import { AppNav, type NavLink } from "../components/athi/AppNav";
import { useNotifications } from "../lib/hooks";

export function DashboardLayout() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();
  
  // Dynamic alerts polling using React Query
  const { data: notificationsResponse } = useNotifications();
  const notifications = notificationsResponse?.items || [];
  const unreadCount = notifications.filter((n) => !n.is_read).length;

  useEffect(() => {
    if (!loading && !user) {
      navigate("/login", { replace: true });
    }
  }, [user, loading, navigate]);

  if (loading || !user) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background text-muted-foreground text-sm font-medium">
        Loading Session context…
      </div>
    );
  }

  // Member menu routes: Restricted to their personal logs & progress
  const memberLinks: NavLink[] = [
    { to: "/dashboard", label: "My Dashboard" },
    { to: "/dashboard/waste", label: "My Waste Records" },
    { to: "/dashboard/payments", label: "My Payments" },
    { to: "/dashboard/notifications", label: "Notifications", badge: unreadCount || undefined },
  ];

  // Leader menu routes: Includes team monitoring & invite managers
  const leaderLinks: NavLink[] = [
    { to: "/dashboard", label: "Dashboard Overview" },
    { to: "/dashboard/team", label: "My Team Roster" },
    { to: "/dashboard/waste", label: "Team Waste Logs" },
    { to: "/dashboard/payments", label: "Milestone Claims" },
    { to: "/dashboard/referrals", label: "Invitation Codes" },
    { to: "/dashboard/notifications", label: "Announcements", badge: unreadCount || undefined },
  ];

  const links = user.role === "MEMBER" ? memberLinks : leaderLinks;

  return (
    <div className="min-h-screen bg-gradient-to-tr from-slate-50 via-slate-100/50 to-blue-50/20 flex flex-col relative overflow-hidden">
      {/* Decorative Dashboard Glowing Auras */}
      <div className="absolute top-[-10%] left-[-15%] w-96 h-96 rounded-full bg-blue-400/5 blur-[80px] animate-pulse-glow pointer-events-none" />
      <div className="absolute bottom-[20%] right-[-10%] w-[400px] h-[400px] rounded-full bg-emerald-400/5 blur-[90px] animate-pulse-glow pointer-events-none" style={{ animationDelay: '-4s' }} />

      {/* Role view banners */}
      {user.role === "MEMBER" ? (
        <div className="bg-primary-soft border-b border-primary/10 px-4 py-2.5 text-center text-xs font-bold text-primary tracking-wide z-10">
          👤 Citizen Member View — Recycle resources, level up personal achievements, and track claims
        </div>
      ) : (
        <div className="bg-success-soft border-b border-success/10 px-4 py-2.5 text-center text-xs font-bold text-success tracking-wide z-10">
          🌟 Team Leader View — Recruit citizens, manage local team milestones, and review collections
        </div>
      )}
      
      <AppNav links={links} />

      <main className="flex-1 mx-auto max-w-7xl w-full px-6 py-8 relative z-10 animate-fade-in-up">
        <Outlet />
      </main>
    </div>
  );
}
export default DashboardLayout;
