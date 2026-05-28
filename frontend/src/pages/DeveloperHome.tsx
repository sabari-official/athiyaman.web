import { Link } from "react-router-dom";
import { Activity, ArrowRight } from "lucide-react";
import { useAuth } from "../lib/auth";

export function DeveloperHome() {
  const { user, signOut } = useAuth();

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-6">
      <div className="w-full max-w-2xl rounded-3xl border border-border bg-card shadow-card overflow-hidden">
        <div className="bg-gradient-to-br from-slate-900 to-primary text-white p-7">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white/15 backdrop-blur">
              <Activity className="h-6 w-6" />
            </div>
            <div>
              <p className="text-xs text-white/70 font-semibold">Developer Monitoring</p>
              <h1 className="text-2xl font-extrabold tracking-tight">Athiyaman Developer</h1>
            </div>
          </div>
          <p className="mt-4 text-sm text-white/80 max-w-xl">
            Placeholder for telemetry dashboards, feature flags, system logs, and health probes.
          </p>
        </div>

        <div className="p-7 space-y-6">
          <div className="rounded-2xl border border-border bg-muted/25 p-5">
            <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">Signed in as</p>
            <p className="mt-1 text-sm font-extrabold text-foreground">
              {user?.username} <span className="text-muted-foreground font-semibold">({user?.role})</span>
            </p>
          </div>

          <div className="grid sm:grid-cols-2 gap-4 text-sm">
            <Link
              to="/dashboard"
              className="h-11 px-4 rounded-xl border border-border bg-white hover:bg-slate-50 font-bold flex items-center justify-between transition"
            >
              Go to Dashboard <ArrowRight className="h-4 w-4" />
            </Link>
            <button
              onClick={() => signOut()}
              className="h-11 px-4 rounded-xl bg-primary text-white font-bold hover:opacity-95 transition"
            >
              Sign out
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DeveloperHome;
