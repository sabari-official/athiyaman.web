import React, { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Leaf, User, Phone, Lock, Gift, ArrowRight, ShieldCheck, Mail, Loader2, AlertCircle, ArrowLeft, Timer, CheckCircle } from "lucide-react";
import { api, apiError } from "../lib/api";
import { useAuth } from "../lib/auth";
import { toast } from "sonner";

export function Signup() {
  const navigate = useNavigate();
  const { signIn } = useAuth();
  
  // States
  const [referralCode, setReferralCode] = useState("");
  const [fullName, setFullName] = useState("");
  const [emailOrPhone, setEmailOrPhone] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  
  // Validation States
  const [usernameAvailable, setUsernameAvailable] = useState<boolean | null>(null);
  const [isCheckingUsername, setIsCheckingUsername] = useState(false);
  const [usernameError, setUsernameError] = useState<string | null>(null);
  const [passwordError, setPasswordError] = useState<string | null>(null);
  const [confirmPasswordError, setConfirmPasswordError] = useState<string | null>(null);
  const [emailOrPhoneError, setEmailOrPhoneError] = useState<string | null>(null);
  const [referralError, setReferralError] = useState<string | null>(null);
  const [nameError, setNameError] = useState<string | null>(null);
  
  // OTP States
  const [otpSent, setOtpSent] = useState(false);
  const [otpCode, setOtpCode] = useState("");
  const [otpInput, setOtpInput] = useState("");
  const [otpTimer, setOtpTimer] = useState(0);
  const [otpVerified, setOtpVerified] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Live Username Uniqueness Check
  useEffect(() => {
    if (!username.trim()) {
      setUsernameAvailable(null);
      setUsernameError(null);
      return;
    }
    if (!/^[a-zA-Z0-9_]+$/.test(username)) {
      setUsernameAvailable(false);
      setUsernameError("Username must contain only letters, numbers, and underscores.");
      return;
    }
    setUsernameError(null);

    const checkAvailability = setTimeout(async () => {
      setIsCheckingUsername(true);
      try {
        const { data } = await api.get(`/auth/check-username?username=${username}`);
        setUsernameAvailable(data.available);
      } catch (e) {
        console.error("Uniqueness check failed", e);
      } finally {
        setIsCheckingUsername(false);
      }
    }, 400); // 400ms debounce

    return () => clearTimeout(checkAvailability);
  }, [username]);

  // OTP Countdown Timer
  useEffect(() => {
    if (otpTimer > 0) {
      const interval = setInterval(() => {
        setOtpTimer((prev) => prev - 1);
      }, 1000);
      return () => clearInterval(interval);
    } else if (otpTimer === 0 && otpSent && !otpVerified) {
      toast.error("OTP has expired. Please request a new one.");
      setOtpSent(false);
      setOtpCode("");
    }
  }, [otpTimer, otpSent, otpVerified]);

  // Send Mock OTP Flow
  const handleGetOtp = () => {
    setEmailOrPhoneError(null);
    if (!emailOrPhone.trim()) {
      setEmailOrPhoneError("Email or Phone number is required.");
      return;
    }

    const isEmail = emailOrPhone.includes("@");
    if (isEmail) {
      if (!/\S+@\S+\.\S+/.test(emailOrPhone)) {
        setEmailOrPhoneError("Invalid email format.");
        return;
      }
    } else {
      const digits = emailOrPhone.replace(/\D/g, "");
      if (digits.length !== 10) {
        setEmailOrPhoneError("Phone number must be exactly 10 numeric digits.");
        return;
      }
    }

    // Trigger OTP sending
    setLoading(true);
    setTimeout(() => {
      const mockCode = String(Math.floor(100000 + Math.random() * 900000));
      setOtpCode(mockCode);
      setOtpSent(true);
      setOtpTimer(60);
      setOtpVerified(false);
      setLoading(false);
      
      toast.success(`Simulated OTP sent to ${emailOrPhone}!`);
      // Display the code dynamically in an alert toast to help the developer/user test easily
      toast.info(`[DEMO CODE]: Your 6-digit OTP code is: ${mockCode}`, { duration: 15000 });
    }, 800);
  };

  // Verify OTP Code
  const handleVerifyOtp = () => {
    if (otpInput === otpCode && otpTimer > 0) {
      setOtpVerified(true);
      toast.success("OTP Code verified successfully!");
    } else {
      toast.error("Incorrect OTP code. Please try again.");
    }
  };

  const validateForm = () => {
    let isValid = true;
    setNameError(null);
    setEmailOrPhoneError(null);
    setReferralError(null);
    setPasswordError(null);
    setConfirmPasswordError(null);

    if (!referralCode.trim()) {
      setReferralError("Referral code is required.");
      isValid = false;
    }
    if (!fullName.trim()) {
      setNameError("Full Name is required.");
      isValid = false;
    }
    if (!username.trim()) {
      setUsernameError("Username is required.");
      isValid = false;
    } else if (usernameAvailable === false) {
      setUsernameError("This username is already taken.");
      isValid = false;
    }

    // Strict 6 characters password validation
    if (password.length !== 6) {
      setPasswordError("Password must be exactly 6 characters.");
      isValid = false;
    }
    if (password !== confirmPassword) {
      setConfirmPasswordError("Passwords do not match.");
      isValid = false;
    }
    if (!otpVerified) {
      toast.error("Please complete the OTP verification before signing up.");
      isValid = false;
    }

    return isValid;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!validateForm()) {
      return;
    }

    setLoading(true);
    try {
      let phoneValue = "";
      let emailValue = "";
      const isEmail = emailOrPhone.includes("@");
      
      if (isEmail) {
        emailValue = emailOrPhone;
        // Generate unique 10-digit phone number to satisfy DB constraint
        const hash = Math.abs(username.split("").reduce((a, b) => ((a << 5) - a) + b.charCodeAt(0), 0));
        phoneValue = "0" + String(hash).padStart(9, "0").substring(0, 9);
      } else {
        phoneValue = emailOrPhone;
      }

      // 1. Submit Citizen Registration
      await api.post("/auth/signup", {
        username: username.trim(),
        phone_number: phoneValue,
        password: password,
        referral_code: referralCode.trim().toUpperCase(),
      });

      // 2. Automate login to issue JWT tokens
      const u = await signIn(username.trim(), password);

      // 3. Prepopulate Name and Email in profile
      await api.put("/profiles/me", {
        full_name: fullName.trim(),
        email: emailValue || null,
      });

      toast.success("Citizen signup completed successfully! Welcome to Athiyaman Portal.");
      
      // 4. Directly route straight to dashboard
      const dest = u.role === "ADMIN" ? "/admin" : u.role === "DEVELOPER" ? "/developer" : "/dashboard";
      navigate(dest, { replace: true });
    } catch (err) {
      setError(apiError(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen grid md:grid-cols-12 bg-background relative overflow-hidden">
      {/* Decorative Aura Spotlights */}
      <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] rounded-full bg-blue-500/5 blur-[100px] animate-pulse-glow pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] rounded-full bg-emerald-500/5 blur-[100px] animate-pulse-glow pointer-events-none" style={{ animationDelay: '-3s' }} />

      {/* Left panel - branding info */}
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
            Verify & Join a Local Team.
          </h1>
          <p className="text-white/85 leading-relaxed text-sm font-medium">
            Signups are closed-loop. To maintain high community integrity, you must obtain a valid single-use invitation code from an active Team Leader or Administrator.
          </p>

          <div className="mt-8 p-6 bg-white/10 backdrop-blur rounded-[24px] border border-white/15 shadow-sm">
            <h4 className="font-extrabold flex items-center gap-2 text-sm text-amber-300 uppercase tracking-wider">
              🇮🇳 Government Resource Scheme
            </h4>
            <p className="mt-3 text-xs text-white/80 leading-relaxed font-medium">
              After a quick signup, you will directly enter your dashboard. To claim waste collection rewards, you'll need to submit profile verification including Aadhaar and payout details.
            </p>
          </div>
        </div>

        <div className="relative text-white/75 text-xs space-y-4 pt-6 border-t border-white/10">
          <p className="italic font-bold">"கழிவுகளை மாற்றுவோம், வாழ்க்கையை மேம்படுத்துவோம்"</p>
          <p className="opacity-50">© 2026 Athiyaman Digital India</p>
        </div>
      </div>

      {/* Right panel form - Crystal Glass scroll panel */}
      <div className="md:col-span-7 flex items-center justify-center p-6 sm:p-10 relative z-10 overflow-y-auto max-h-screen">
        <div className="w-full max-w-xl bg-white/90 backdrop-blur-lg border border-slate-200/80 p-8 sm:p-10 rounded-[36px] shadow-2xl relative overflow-hidden animate-fade-in-up gov-tricolor-bar">
          
          {/* Elegant Back button at top-right */}
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="absolute right-6 top-6 flex items-center gap-1.5 text-xs font-bold text-slate-500 hover:text-slate-800 transition"
          >
            <ArrowLeft className="h-3.5 w-3.5" /> Back
          </button>

          <h2 className="text-3xl font-black text-slate-800 tracking-tight leading-none">Register Account 🌟</h2>
          <p className="mt-3 text-slate-500 text-xs font-semibold uppercase tracking-wider">Enter your referral code and complete verification</p>

          <form onSubmit={handleSubmit} className="mt-8 space-y-6">
            
            {/* Core Sign-up parameters */}
            <div className="space-y-4">
              <h3 className="text-xs font-black uppercase tracking-widest text-slate-400 border-b border-slate-100 pb-2 flex items-center gap-1.5">
                🔑 Registration Details
              </h3>
              <div className="grid sm:grid-cols-2 gap-4">
                <Field label="Referral Invitation Code" required>
                  <div className="relative mt-1.5">
                    <Gift className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-slate-400" />
                    <input
                      type="text"
                      required
                      value={referralCode}
                      onChange={(e) => setReferralCode(e.target.value)}
                      className={`input-field pl-11 h-11 font-bold tracking-widest uppercase placeholder:font-normal placeholder:tracking-normal ${referralError ? "border-red-400" : ""}`}
                      placeholder="e.g. LDRX12"
                    />
                  </div>
                  {referralError && <p className="text-xs text-red-500 mt-1 font-semibold">{referralError}</p>}
                </Field>

                <Field label="Full Name" required>
                  <div className="relative mt-1.5">
                    <User className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-slate-400" />
                    <input
                      type="text"
                      required
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      className={`input-field pl-11 h-11 ${nameError ? "border-red-400" : ""}`}
                      placeholder="Enter full name"
                    />
                  </div>
                  {nameError && <p className="text-xs text-red-500 mt-1 font-semibold">{nameError}</p>}
                </Field>

                <div className="sm:col-span-2">
                  <Field label="Email Address or Phone Number" required>
                    <div className="relative mt-1.5">
                      <Mail className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-slate-400" />
                      <input
                        type="text"
                        required
                        value={emailOrPhone}
                        disabled={otpSent}
                        onChange={(e) => setEmailOrPhone(e.target.value)}
                        className={`input-field pl-11 pr-24 h-11 ${emailOrPhoneError ? "border-red-400 bg-red-50/20" : ""}`}
                        placeholder="you@email.com or 10-digit phone"
                      />
                      {!otpSent && (
                        <button
                          type="button"
                          onClick={handleGetOtp}
                          disabled={loading}
                          className="absolute right-1.5 top-1/2 -translate-y-1/2 px-3 py-1.5 rounded-xl bg-primary text-white text-[10px] font-extrabold uppercase hover:opacity-95 transition"
                        >
                          {loading ? "Sending..." : "Get OTP"}
                        </button>
                      )}
                      {otpSent && (
                        <span className="absolute right-3.5 top-1/2 -translate-y-1/2 text-xs font-bold text-success flex items-center gap-1">
                          <CheckCircle className="h-4.5 w-4.5" /> Sent
                        </span>
                      )}
                    </div>
                    {emailOrPhoneError && (
                      <p className="text-xs text-red-500 mt-1 font-semibold flex items-center gap-1">
                        <AlertCircle className="h-3.5 w-3.5" /> {emailOrPhoneError}
                      </p>
                    )}
                  </Field>
                </div>

                {/* OTP Verification Countdown Drawer */}
                {otpSent && (
                  <div className="sm:col-span-2 p-5 rounded-2xl bg-amber-50/40 border border-amber-200/50 space-y-3 animate-fade-in-up">
                    <div className="flex items-center justify-between text-xs text-slate-600">
                      <span className="font-extrabold flex items-center gap-1">
                        <Timer className="h-4 w-4 text-amber-500 animate-pulse" /> OTP Code Sent
                      </span>
                      <span className="font-bold font-mono">
                        Expires in: <strong className="text-red-500">{otpTimer}s</strong>
                      </span>
                    </div>

                    <div className="flex gap-2">
                      <input
                        type="text"
                        maxLength={6}
                        required
                        disabled={otpVerified}
                        value={otpInput}
                        onChange={(e) => setOtpInput(e.target.value.replace(/\D/g, ""))}
                        className="input-field h-11 text-center font-mono tracking-widest font-black text-lg bg-white"
                        placeholder="••••••"
                      />
                      <button
                        type="button"
                        onClick={handleVerifyOtp}
                        disabled={otpVerified || !otpInput || otpTimer === 0}
                        className="px-6 rounded-xl bg-success text-white font-extrabold text-xs uppercase hover:opacity-95 transition disabled:opacity-50"
                      >
                        {otpVerified ? "Verified" : "Verify"}
                      </button>
                    </div>

                    {!otpVerified && (
                      <p className="text-[10px] text-slate-500 font-medium">
                        Please check your notifications or toast updates for the mock 6-digit OTP code to complete registration.
                      </p>
                    )}
                  </div>
                )}

                <Field label="Unique Username" required>
                  <div className="relative mt-1.5">
                    <User className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-slate-400" />
                    <input
                      type="text"
                      required
                      value={username}
                      onChange={(e) => setUsername(e.target.value.replace(/[^a-zA-Z0-9_]/g, ""))}
                      className={`input-field pl-11 pr-10 h-11 ${
                        usernameAvailable === true ? "border-emerald-500 bg-emerald-50/20" : usernameAvailable === false ? "border-red-400 bg-red-50/20" : ""
                      }`}
                      placeholder="Enter username"
                    />
                    {isCheckingUsername && (
                      <Loader2 className="animate-spin absolute right-3 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-slate-400" />
                    )}
                  </div>
                  {usernameAvailable === true && (
                    <p className="text-[10px] text-emerald-600 mt-1 font-bold">✓ Username is available!</p>
                  )}
                  {usernameError && (
                    <p className="text-xs text-red-500 mt-1 font-semibold flex items-center gap-1">
                      <AlertCircle className="h-3.5 w-3.5" /> {usernameError}
                    </p>
                  )}
                </Field>

                <Field label="Password (exactly 6 chars)" required>
                  <div className="relative mt-1.5">
                    <Lock className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-slate-400" />
                    <input
                      type="password"
                      required
                      maxLength={6}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className={`input-field pl-11 h-11 ${passwordError ? "border-red-400 bg-red-50/20" : ""}`}
                      placeholder="Exactly 6 chars"
                    />
                  </div>
                  {passwordError && (
                    <p className="text-xs text-red-500 mt-1 font-semibold flex items-center gap-1">
                      <AlertCircle className="h-3.5 w-3.5" /> {passwordError}
                    </p>
                  )}
                </Field>

                <Field label="Confirm Password" required>
                  <div className="relative mt-1.5">
                    <Lock className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-slate-400" />
                    <input
                      type="password"
                      required
                      maxLength={6}
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      className={`input-field pl-11 h-11 ${confirmPasswordError ? "border-red-400 bg-red-50/20" : ""}`}
                      placeholder="Repeat password"
                    />
                  </div>
                  {confirmPasswordError && (
                    <p className="text-xs text-red-500 mt-1 font-semibold flex items-center gap-1">
                      <AlertCircle className="h-3.5 w-3.5" /> {confirmPasswordError}
                    </p>
                  )}
                </Field>
              </div>
            </div>

            {error && (
              <div className="rounded-2xl bg-danger-soft text-danger border border-danger/10 text-xs px-4 py-3 font-semibold shadow-sm flex items-start gap-2">
                <AlertCircle className="h-4 w-4 shrink-0 mt-0.5" />
                <span>{error}</span>
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !otpVerified}
              className="w-full h-12 rounded-2xl bg-primary text-white font-extrabold shadow-btn hover:opacity-95 disabled:opacity-50 disabled:cursor-not-allowed transition duration-300 transform hover:-translate-y-0.5 active:scale-95 text-sm tracking-wider uppercase"
            >
              {loading ? "Creating Account…" : "Verify OTP & Complete Signup"}
            </button>

            <div className="flex items-center gap-3 py-1">
              <div className="flex-1 h-px bg-slate-200/60" />
              <span className="text-[10px] text-slate-400 font-extrabold uppercase tracking-widest">already have an account?</span>
              <div className="flex-1 h-px bg-slate-200/60" />
            </div>

            <Link
              to="/login"
              className="flex w-full h-12 items-center justify-center rounded-2xl border-2 border-slate-200 text-slate-500 font-extrabold hover:bg-slate-50 transition duration-300 text-xs uppercase tracking-wider"
            >
              Sign In Instead <ArrowRight className="ml-1.5 h-4 w-4" />
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
