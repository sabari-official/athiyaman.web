import React, { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Leaf, Mail, Lock, Eye, EyeOff, Recycle, TrendingUp, Wallet, AlertCircle, ArrowLeft } from "lucide-react";
import { useAuth } from "../lib/auth";
import { toast } from "sonner";

export function Login() {
  const { user, signIn } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState(() => {
    return localStorage.getItem("remembered_username") || "";
  });
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(() => {
    return localStorage.getItem("remember_me") === "true";
  });
  const [show, setShow] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Field-level error highlights
  const [usernameError, setUsernameError] = useState<string | null>(null);
  const [passwordError, setPasswordError] = useState<string | null>(null);

  useEffect(() => {
    if (user) {
      if (user.role === "ADMIN") {
        navigate("/admin", { replace: true });
      } else if (user.role === "DEVELOPER") {
        navigate("/developer", { replace: true });
      } else {
        navigate("/dashboard", { replace: true });
      }
    }
  }, [user, navigate]);

  const validateForm = () => {
    let isValid = true;
    setUsernameError(null);
    setPasswordError(null);

    // 1. Username/Phone required check
    if (!username.trim()) {
      setUsernameError("Username or Phone number is required.");
      isValid = false;
    } else {
      // If entering only digits, it must be a valid 10-digit Indian phone number
      const digitsOnly = username.replace(/\D/g, "");
      if (/^\d+$/.test(username) && digitsOnly.length !== 10) {
        setUsernameError("Phone number must consist of exactly 10 numeric digits.");
        isValid = false;
      }
    }

    // 2. Password required and length check
    if (!password) {
      setPasswordError("Password is required.");
      isValid = false;
    } else if (password.length < 6) {
      setPasswordError("Password must be at least 6 characters long.");
      isValid = false;
    }

    return isValid;
  };

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!validateForm()) {
      toast.error("Please correct the form errors before signing in.");
      return;
    }

    setLoading(true);
    try {
      const u = await signIn(username.trim(), password);
      
      // Save Remember Me state
      if (rememberMe) {
        localStorage.setItem("remembered_username", username.trim());
        localStorage.setItem("remember_me", "true");
      } else {
        localStorage.removeItem("remembered_username");
        localStorage.setItem("remember_me", "false");
      }

      toast.success(`Welcome back, ${u.username}!`);
      const dest = u.role === "ADMIN" ? "/admin" : u.role === "DEVELOPER" ? "/developer" : "/dashboard";
      navigate(dest, { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Authentication failed. Double check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen grid md:grid-cols-12 bg-background relative overflow-hidden">
      {/* Decorative Aura Spotlights */}
      <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] rounded-full bg-blue-500/5 blur-[100px] animate-pulse-glow pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] rounded-full bg-emerald-500/5 blur-[100px] animate-pulse-glow pointer-events-none" style={{ animationDelay: '-3s' }} />

      {/* Left Brand Panel - Asymmetric Custom Layout */}
      <div className="md:col-span-5 bg-gradient-to-br from-deep-blue to-primary text-white flex flex-col p-10 md:p-14 relative overflow-hidden">
        <div className="absolute -right-20 -top-20 h-72 w-72 rounded-full bg-white/5" />
        <div className="absolute -left-16 bottom-20 h-48 w-48 rounded-full bg-success/10" />

        <div className="relative flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white/15 backdrop-blur border border-white/10 shadow-sm">
            <Leaf className="h-5.5 w-5.5 text-white" />
          </div>
          <span className="text-lg font-black tracking-tight uppercase">Athiyaman</span>
        </div>

        <div className="relative my-auto py-10 space-y-6">
          <h1 className="text-4xl md:text-5.5xl font-black leading-[1.1] tracking-tight">
            Swachh Bharat.<br />Better Tomorrow.
          </h1>
          <p className="text-white/80 leading-relaxed text-sm font-medium">
            Log your collected resource records, sequentially level up personal milestones, and earn financial rewards for keeping India clean.
          </p>

          <ul className="mt-8 space-y-4 max-w-sm pt-6 border-t border-white/10">
            <Feature icon={<Recycle className="h-5 w-5" />} label="Submit Verified Waste Records" />
            <Feature icon={<TrendingUp className="h-5 w-5" />} label="Track Your Level Progress" />
            <Feature icon={<Wallet className="h-5 w-5" />} label="Claim Rupee Milestone Rewards" />
          </ul>
        </div>

        <div className="relative text-white/75 text-xs space-y-4 pt-6 border-t border-white/10">
          <p className="italic font-bold">"கழிவுகளை மாற்றுவோம், வாழ்க்கையை மேம்படுத்துவோம்"</p>
          <p className="opacity-80">Let's transform waste, let's improve life.</p>
          <p className="opacity-50">© 2026 Athiyaman Digital India</p>
        </div>
      </div>

      {/* Right Form Panel - Sleek Floating Glass Panel */}
      <div className="md:col-span-7 flex items-center justify-center p-8 md:p-16 relative z-10">
        <div className="w-full max-w-md bg-white/90 backdrop-blur-lg border border-slate-200/80 p-10 rounded-[36px] shadow-2xl relative overflow-hidden animate-fade-in-up gov-tricolor-bar">
          
          {/* Elegant Back button at top-right */}
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="absolute right-6 top-6 flex items-center gap-1.5 text-xs font-bold text-slate-500 hover:text-slate-800 transition"
          >
            <ArrowLeft className="h-3.5 w-3.5" /> Back
          </button>

          <h2 className="text-3xl font-black text-slate-800 tracking-tight leading-none">Welcome Back! 🙏</h2>
          <p className="mt-3 text-slate-500 text-xs font-semibold uppercase tracking-wider">Please sign in with your account to continue</p>

          <form onSubmit={submit} className="mt-8 space-y-6">
            <Field label="Username or Phone Number" required>
              <div className="relative mt-1.5">
                <Mail className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-slate-400" />
                <input
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className={`input-field pl-11 h-12 ${usernameError ? "border-red-400 bg-red-50/20" : ""}`}
                  placeholder="Enter username or phone number"
                />
              </div>
              {usernameError && (
                <p className="text-xs text-red-500 mt-1 font-semibold flex items-center gap-1">
                  <AlertCircle className="h-3.5 w-3.5" /> {usernameError}
                </p>
              )}
            </Field>

            <Field label="Password" required>
              <div className="relative mt-1.5">
                <Lock className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-slate-400" />
                <input
                  type={show ? "text" : "password"}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className={`input-field pl-11 pr-12 h-12 ${passwordError ? "border-red-400 bg-red-50/20" : ""}`}
                  placeholder="••••••••"
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
              {passwordError && (
                <p className="text-xs text-red-500 mt-1 font-semibold flex items-center gap-1">
                  <AlertCircle className="h-3.5 w-3.5" /> {passwordError}
                </p>
              )}
            </Field>

            {/* Remember Me */}
            <div className="flex items-center justify-between py-1">
              <label className="flex items-center gap-2 cursor-pointer select-none">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="rounded text-primary focus:ring-primary h-4.5 w-4.5 cursor-pointer accent-primary"
                />
                <span className="text-xs font-bold text-slate-600">Remember me</span>
              </label>
            </div>

            {error && (
              <div className="rounded-2xl bg-danger-soft text-danger border border-danger/10 text-xs px-4 py-3 font-semibold shadow-sm flex items-start gap-2">
                <AlertCircle className="h-4 w-4 shrink-0 mt-0.5" />
                <span>{error}</span>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full h-12 rounded-2xl bg-primary text-white font-extrabold shadow-btn hover:opacity-95 disabled:opacity-60 transition duration-300 transform hover:-translate-y-0.5 active:scale-95 text-sm tracking-wider uppercase"
            >
              {loading ? "Signing in…" : "Sign In"}
            </button>

            <div className="flex items-center gap-3 py-2">
              <div className="flex-1 h-px bg-slate-200/60" />
              <span className="text-[10px] text-slate-400 font-extrabold uppercase tracking-widest">or</span>
              <div className="flex-1 h-px bg-slate-200/60" />
            </div>

            <Link
              to="/signup"
              className="flex w-full h-12 items-center justify-center rounded-2xl border-2 border-primary/20 text-primary font-extrabold hover:bg-primary-soft transition duration-300 text-xs uppercase tracking-wider"
            >
              Register with Referral Code
            </Link>
          </form>
        </div>
      </div>
    </div>
  );
}

function Field({ label, required, children }: { label: string; required?: boolean; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="text-xs font-bold text-slate-700 flex items-center gap-1">
        {label} {required && <span className="text-danger">*</span>}
      </span>
      {children}
    </label>
  );
}

function Feature({ icon, label }: { icon: React.ReactNode; label: string }) {
  return (
    <li className="flex items-center gap-4">
      <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white/10 backdrop-blur shadow-sm border border-white/5">{icon}</div>
      <span className="font-semibold text-sm">{label}</span>
    </li>
  );
}
