import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ShieldAlert, Lock, User, Eye, EyeOff } from "lucide-react";
import { api, apiError } from "../lib/api";
import { useAuth } from "../lib/auth";
import { toast } from "sonner";

export function ChangePassword() {
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [newUsername, setNewUsername] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [show, setShow] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // 1. Client-side validations
    if (newUsername.trim() && !/^[a-zA-Z0-9_]+$/.test(newUsername)) {
      setError("Username must contain only letters, numbers, and underscores.");
      return;
    }

    if (newPassword.length < 6) {
      setError("New password must be at least 6 characters long.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setError("Passwords do not match. Please verify your entries.");
      return;
    }

    if (currentPassword === newPassword) {
      setError("New password cannot be identical to your current password.");
      return;
    }

    setLoading(true);
    try {
      // Endpoint: POST /api/v1/auth/change-password
      await api.post("/auth/change-password", {
        current_password: currentPassword,
        new_password: newPassword,
        new_username: newUsername.trim() || undefined,
      });

      toast.success("Security credentials updated successfully!");
      
      // Successfully updated -> Route user to correct dashboard panel
      const dest = user?.role === "ADMIN" ? "/admin" : user?.role === "DEVELOPER" ? "/developer" : "/dashboard";
      navigate(dest, { replace: true });
    } catch (err) {
      setError(apiError(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-6 relative overflow-hidden">
      {/* Tricolor Background Accent Spotlights */}
      <div className="absolute top-[-10%] left-[-10%] w-[300px] h-[300px] rounded-full bg-amber-500/5 blur-[80px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[300px] h-[300px] rounded-full bg-emerald-500/5 blur-[80px] pointer-events-none" />

      <div className="w-full max-w-md bg-white/95 backdrop-blur-lg border border-slate-200/85 p-8 rounded-[32px] shadow-2xl relative overflow-hidden gov-tricolor-bar animate-fade-in-up">
        <div className="flex flex-col items-center text-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-warning-soft text-warning">
            <ShieldAlert className="h-6 w-6" />
          </div>
          <h2 className="mt-4 text-2xl font-extrabold text-slate-800 tracking-tight">Security Credentials Update</h2>
          <p className="mt-1.5 text-xs text-slate-500 max-w-xs leading-relaxed">
            As an Administrator or Developer logging in with **temporary credentials**, you must establish a permanent custom username and strong passcode to proceed safely.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="mt-8 space-y-5">
          <Field label="Configure New Username">
            <div className="relative mt-1.5">
              <User className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
              <input
                type="text"
                required
                value={newUsername}
                onChange={(e) => setNewUsername(e.target.value.replace(/[^a-zA-Z0-9_]/g, ""))}
                className="input-field pl-11 h-11"
                placeholder="Enter permanent username"
              />
            </div>
          </Field>

          <Field label="Temporary Password (Current)">
            <div className="relative mt-1.5">
              <Lock className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
              <input
                type={show ? "text" : "password"}
                required
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                className="input-field pl-11 h-11"
                placeholder="Enter temporary password"
              />
            </div>
          </Field>

          <Field label="New Password (Min 6 chars)">
            <div className="relative mt-1.5">
              <Lock className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
              <input
                type={show ? "text" : "password"}
                required
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                className="input-field pl-11 pr-12 h-11"
                placeholder="Enter strong password"
              />
              <button
                type="button"
                onClick={() => setShow((s) => !s)}
                className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition p-1"
                aria-label={show ? "Hide password" : "Show password"}
              >
                {show ? <EyeOff className="h-4.5 w-4.5" /> : <Eye className="h-4.5 w-4.5" />}
              </button>
            </div>
          </Field>

          <Field label="Confirm New Password">
            <div className="relative mt-1.5">
              <Lock className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
              <input
                type={show ? "text" : "password"}
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="input-field pl-11 h-11"
                placeholder="Confirm your new password"
              />
            </div>
          </Field>

          {error && (
            <div className="rounded-xl bg-danger-soft text-danger border border-danger/10 text-xs px-4 py-3 font-semibold shadow-sm">
              ⚠️ {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full h-12 rounded-xl bg-primary text-white font-extrabold shadow-btn hover:opacity-95 disabled:opacity-60 transition"
          >
            {loading ? "Saving Credentials…" : "Overwrite Onboarding Credentials"}
          </button>
        </form>
      </div>
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="text-xs font-bold text-slate-700">{label}</span>
      {children}
    </label>
  );
}
