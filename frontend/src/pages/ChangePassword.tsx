import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ShieldAlert, Lock, Eye, EyeOff } from "lucide-react";
import { api, apiError } from "../lib/api";
import { toast } from "sonner";

export function ChangePassword() {
  const navigate = useNavigate();
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [show, setShow] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // 1. Client-side length checks
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
      });

      toast.success("Security password changed successfully!");
      
      // Successfully updated -> Route user to dashboard panel
      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(apiError(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-6">
      <div className="w-full max-w-md bg-card border border-border rounded-2xl shadow-card p-6 md:p-8">
        <div className="flex flex-col items-center text-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-warning-soft text-warning">
            <ShieldAlert className="h-6 w-6" />
          </div>
          <h2 className="mt-4 text-2xl font-extrabold text-foreground tracking-tight">Security Passcode Update</h2>
          <p className="mt-1.5 text-sm text-muted-foreground max-w-xs">
            To ensure complete security of bank profiles and claims, you are required to configure a strong password to continue.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="mt-8 space-y-5">
          <Field label="Current Password">
            <div className="relative">
              <Lock className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                type={show ? "text" : "password"}
                required
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                className="w-full h-12 rounded-xl border border-border bg-white pl-11 pr-3 text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary shadow-card transition-all"
                placeholder="Enter current password"
              />
            </div>
          </Field>

          <Field label="New Password">
            <div className="relative">
              <Lock className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                type={show ? "text" : "password"}
                required
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                className="w-full h-12 rounded-xl border border-border bg-white pl-11 pr-12 text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary shadow-card transition-all"
                placeholder="•••••••• (Min 6 characters)"
              />
              <button
                type="button"
                onClick={() => setShow((s) => !s)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition p-1"
                aria-label={show ? "Hide password" : "Show password"}
              >
                {show ? <EyeOff className="h-4.5 w-4.5" /> : <Eye className="h-4.5 w-4.5" />}
              </button>
            </div>
          </Field>

          <Field label="Confirm New Password">
            <div className="relative">
              <Lock className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                type={show ? "text" : "password"}
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full h-12 rounded-xl border border-border bg-white pl-11 pr-3 text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary shadow-card transition-all"
                placeholder="Confirm your new password"
              />
            </div>
          </Field>

          {error && (
            <div className="rounded-xl bg-danger-soft text-danger border border-danger/10 text-xs px-4 py-3 font-semibold">
              ⚠️ {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full h-12 rounded-xl bg-primary text-white font-bold shadow-btn hover:opacity-95 disabled:opacity-60 transition"
          >
            {loading ? "Updating Passcode…" : "Update Password & Continue"}
          </button>
        </form>
      </div>
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="text-sm font-semibold text-foreground">{label}</span>
      <div className="mt-1.5">{children}</div>
    </label>
  );
}
