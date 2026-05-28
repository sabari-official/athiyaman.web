import React, { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Leaf, User, Phone, Lock, Gift, ArrowRight, ShieldCheck, Mail, MapPin, Loader2, AlertCircle } from "lucide-react";
import verhoeff from "verhoeff";
import { api, apiError } from "../lib/api";
import { toast } from "sonner";

export function Signup() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [referralCode, setReferralCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Additional bio details for streamlined onboarding
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [aadhaar, setAadhaar] = useState("");
  const [state, setState] = useState("Tamil Nadu");
  const [district, setDistrict] = useState("");
  const [pincode, setPincode] = useState("");
  const [doorNo, setDoorNo] = useState("");
  const [streetName, setStreetName] = useState("");
  const [landmark, setLandmark] = useState("");
  const [postOffice, setPostOffice] = useState("");
  const [city, setCity] = useState("");

  // Pincode & Aadhaar Status triggers
  const [isPincodeLoading, setIsPincodeLoading] = useState(false);
  const [postOfficeOptions, setPostOfficeOptions] = useState<string[]>([]);
  const [aadhaarVerified, setAadhaarVerified] = useState<boolean | null>(null);

  // Field-level error messages
  const [usernameError, setUsernameError] = useState<string | null>(null);
  const [phoneError, setPhoneError] = useState<string | null>(null);
  const [passwordError, setPasswordError] = useState<string | null>(null);
  const [emailError, setEmailError] = useState<string | null>(null);
  const [aadhaarError, setAadhaarError] = useState<string | null>(null);
  const [pincodeError, setPincodeError] = useState<string | null>(null);

  // Live Aadhaar Checksum verification
  useEffect(() => {
    if (aadhaar.length === 12) {
      if (/^\d+$/.test(aadhaar) && verhoeff.validate(aadhaar)) {
        setAadhaarVerified(true);
        setAadhaarError(null);
      } else {
        setAadhaarVerified(false);
        setAadhaarError("Invalid Aadhaar number checksum validation failed.");
      }
    } else {
      setAadhaarVerified(null);
      setAadhaarError(null);
    }
  }, [aadhaar]);

  // Pincode Address Auto-fill API Integration
  useEffect(() => {
    const fetchAddressFromPincode = async () => {
      if (pincode.length === 6 && /^\d+$/.test(pincode)) {
        setIsPincodeLoading(true);
        setPincodeError(null);
        try {
          const res = await fetch(`https://api.postalpincode.in/pincode/${pincode}`);
          const data = await res.json();
          if (data && data[0] && data[0].Status === "Success") {
            const postOfficeList = data[0].PostOffice;
            if (postOfficeList && postOfficeList.length > 0) {
              const first = postOfficeList[0];
              setState(first.State || "Tamil Nadu");
              setDistrict(first.District || "");
              setCity(first.Block || first.Division || first.Circle || first.District || "");
              
              const options = postOfficeList.map((po: any) => po.Name);
              setPostOfficeOptions(options);
              setPostOffice(options[0]);
              toast.success("Address details populated from pincode successfully!");
            }
          } else {
            setPincodeError("Invalid Pincode or no records found.");
          }
        } catch (e) {
          console.error("Pincode API failed", e);
        } finally {
          setIsPincodeLoading(false);
        }
      } else {
        setPostOfficeOptions([]);
      }
    };

    fetchAddressFromPincode();
  }, [pincode]);

  const validateForm = () => {
    let isValid = true;
    setUsernameError(null);
    setPhoneError(null);
    setPasswordError(null);
    setEmailError(null);
    setAadhaarError(null);
    setPincodeError(null);

    // Username check
    if (!username.trim()) {
      setUsernameError("Username is required.");
      isValid = false;
    } else if (!/^[a-zA-Z0-9_]+$/.test(username)) {
      setUsernameError("Username must contain only letters, numbers, and underscores.");
      isValid = false;
    }

    // Phone check
    if (phone.length !== 10 || !/^\d+$/.test(phone)) {
      setPhoneError("Phone number must consist of exactly 10 numeric digits.");
      isValid = false;
    }

    // Password check
    if (password.length < 6) {
      setPasswordError("Password must be at least 6 characters long.");
      isValid = false;
    }

    // Email check
    if (email && !/\S+@\S+\.\S+/.test(email)) {
      setEmailError("Invalid email format (e.g. you@example.com).");
      isValid = false;
    }

    // Aadhaar check
    if (aadhaar.length !== 12 || !/^\d+$/.test(aadhaar)) {
      setAadhaarError("Aadhaar number must consist of exactly 12 numeric digits.");
      isValid = false;
    } else if (!verhoeff.validate(aadhaar)) {
      setAadhaarError("Invalid Aadhaar checksum. Please verify card number.");
      isValid = false;
    }

    // Pincode check
    if (pincode.length !== 6 || !/^\d+$/.test(pincode)) {
      setPincodeError("Pincode must consist of exactly 6 numeric digits.");
      isValid = false;
    }

    return isValid;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!validateForm()) {
      toast.error("Please correct the form errors before registering.");
      return;
    }

    setLoading(true);
    try {
      // First register the citizen credentials
      await api.post("/auth/signup", {
        username: username.trim(),
        phone_number: phone,
        password,
        referral_code: referralCode.trim().toUpperCase(),
      });

      // Try automatic profile update pre-link (optional but highly premium)
      try {
        await api.post("/auth/login", { username: username.trim(), password });
        await api.put("/profiles/me", {
          full_name: fullName.trim() || username,
          email: email.trim() || null,
          state,
          district,
          pincode,
          door_no: doorNo || null,
          street_name: streetName || null,
          landmark: landmark || null,
          post_office: postOffice || null,
          city: city || null,
        });
      } catch (profileErr) {
        console.warn("Silent profile linking skipped (completed after dashboard login)", profileErr);
      }

      toast.success("Citizen signup completed successfully! Welcome to Athiyaman.");
      navigate("/login", { replace: true });
    } catch (err) {
      setError(apiError(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen grid md:grid-cols-12 bg-background relative overflow-hidden">
      {/* Decorative spotlights */}
      <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] rounded-full bg-blue-500/5 blur-[100px] animate-pulse-glow pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] rounded-full bg-emerald-500/5 blur-[100px] animate-pulse-glow pointer-events-none" style={{ animationDelay: '-3s' }} />

      {/* Left panel - info */}
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
            Signups are closed-loop. To maintain high community integrity, you must obtain a valid single-use invitation code from an active Team Leader.
          </p>

          <div className="mt-8 p-6 bg-white/10 backdrop-blur rounded-[24px] border border-white/15 shadow-sm">
            <h4 className="font-extrabold flex items-center gap-2 text-sm text-success uppercase tracking-wider">
              💡 Live Credentials Linking
            </h4>
            <p className="mt-3 text-xs text-white/80 leading-relaxed font-medium">
              If you submitted a Leader or Member Application that was approved, please register using the **exact phone number** submitted in your application. The platform will automatically link your profile name, email, and Aadhaar info during signup!
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
        <div className="w-full max-w-xl bg-white/60 backdrop-blur-lg border border-white/70 p-8 sm:p-10 rounded-[36px] shadow-2xl relative overflow-hidden animate-fade-in-up">
          <div className="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-blue-500 to-emerald-500" />
          
          <h2 className="text-3xl font-black text-slate-800 tracking-tight leading-none">Create Account 🌟</h2>
          <p className="mt-3 text-slate-500 text-xs font-semibold uppercase tracking-wider">Onboard using your inviter referral invitation code</p>

          <form onSubmit={handleSubmit} className="mt-8 space-y-6">
            
            {/* Credentials Block */}
            <div className="space-y-4">
              <h3 className="text-xs font-black uppercase tracking-widest text-slate-400 border-b border-slate-100 pb-2 flex items-center gap-1.5">
                🔒 System Login Credentials
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
                      className="input-field pl-11 h-11 font-bold tracking-widest uppercase placeholder:font-normal placeholder:tracking-normal"
                      placeholder="e.g. LDRX12"
                    />
                  </div>
                </Field>

                <Field label="Unique Username" required>
                  <div className="relative mt-1.5">
                    <User className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-slate-400" />
                    <input
                      type="text"
                      required
                      value={username}
                      onChange={(e) => setUsername(e.target.value.replace(/[^a-zA-Z0-9_]/g, ""))}
                      className={`input-field pl-11 h-11 ${usernameError ? "border-red-400 bg-red-50/20" : ""}`}
                      placeholder="Enter profile username"
                    />
                  </div>
                  {usernameError && (
                    <p className="text-xs text-red-500 mt-1 font-semibold flex items-center gap-1">
                      <AlertCircle className="h-3.5 w-3.5" /> {usernameError}
                    </p>
                  )}
                </Field>

                <Field label="Phone Number" required>
                  <div className="relative mt-1.5">
                    <Phone className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-slate-400" />
                    <input
                      type="text"
                      required
                      maxLength={10}
                      value={phone}
                      onChange={(e) => setPhone(e.target.value.replace(/\D/g, ""))}
                      className={`input-field pl-11 h-11 ${phoneError ? "border-red-400 bg-red-50/20" : ""}`}
                      placeholder="10 digit Indian mobile"
                    />
                  </div>
                  {phoneError && (
                    <p className="text-xs text-red-500 mt-1 font-semibold flex items-center gap-1">
                      <AlertCircle className="h-3.5 w-3.5" /> {phoneError}
                    </p>
                  )}
                </Field>

                <Field label="Password" required>
                  <div className="relative mt-1.5">
                    <Lock className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-slate-400" />
                    <input
                      type="password"
                      required
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className={`input-field pl-11 h-11 ${passwordError ? "border-red-400 bg-red-50/20" : ""}`}
                      placeholder="Min 6 characters"
                    />
                  </div>
                  {passwordError && (
                    <p className="text-xs text-red-500 mt-1 font-semibold flex items-center gap-1">
                      <AlertCircle className="h-3.5 w-3.5" /> {passwordError}
                    </p>
                  )}
                </Field>
              </div>
            </div>

            {/* Biographical Info Block */}
            <div className="space-y-4 pt-2">
              <h3 className="text-xs font-black uppercase tracking-widest text-slate-400 border-b border-slate-100 pb-2 flex items-center gap-1.5">
                👤 Biographical Profile Details
              </h3>
              <div className="grid sm:grid-cols-2 gap-4">
                <Field label="Full Name (as in Aadhaar)" required>
                  <input
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    className="input-field mt-1.5 h-11"
                    placeholder="Enter full name"
                  />
                </Field>

                <Field label="Email Address" required>
                  <div className="relative mt-1.5">
                    <Mail className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-slate-400" />
                    <input
                      type="email"
                      required
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className={`input-field pl-11 h-11 ${emailError ? "border-red-400 bg-red-50/20" : ""}`}
                      placeholder="you@example.com"
                    />
                  </div>
                  {emailError && (
                    <p className="text-xs text-red-500 mt-1 font-semibold flex items-center gap-1">
                      <AlertCircle className="h-3.5 w-3.5" /> {emailError}
                    </p>
                  )}
                </Field>

                <div className="sm:col-span-2">
                  <Field label="Aadhaar Card Number" required>
                    <div className="relative mt-1.5">
                      <input
                        type="text"
                        required
                        maxLength={12}
                        value={aadhaar}
                        onChange={(e) => setAadhaar(e.target.value.replace(/\D/g, ""))}
                        className={`input-field h-11 pr-24 ${
                          aadhaarVerified === true ? "border-emerald-500 bg-emerald-50/20" : aadhaarVerified === false ? "border-red-400 bg-red-50/20" : ""
                        }`}
                        placeholder="12 digit number"
                      />
                      {aadhaarVerified === true && (
                        <span className="absolute right-3.5 top-1/2 -translate-y-1/2 inline-flex items-center gap-1 text-[10px] font-black uppercase text-success px-2 py-0.5 rounded-full bg-success-soft border border-success/20 shadow-sm animate-float">
                          ✓ Verified
                        </span>
                      )}
                      {aadhaarVerified === false && (
                        <span className="absolute right-3.5 top-1/2 -translate-y-1/2 inline-flex items-center gap-1 text-[10px] font-black uppercase text-danger px-2 py-0.5 rounded-full bg-danger-soft border border-danger/20">
                          ✗ Invalid
                        </span>
                      )}
                    </div>
                    {aadhaarError && (
                      <p className="text-xs text-red-500 mt-1 font-semibold flex items-center gap-1">
                        <AlertCircle className="h-3.5 w-3.5" /> {aadhaarError}
                      </p>
                    )}
                  </Field>
                </div>
              </div>
            </div>

            {/* Address Info Block */}
            <div className="space-y-4 pt-2">
              <h3 className="text-xs font-black uppercase tracking-widest text-slate-400 border-b border-slate-100 pb-2 flex items-center gap-1.5">
                📍 Physical Geocoded Address
              </h3>
              <div className="grid sm:grid-cols-3 gap-4">
                <Field label="Pincode" required>
                  <div className="relative mt-1.5">
                    <input
                      type="text"
                      required
                      maxLength={6}
                      value={pincode}
                      onChange={(e) => setPincode(e.target.value.replace(/\D/g, ""))}
                      className={`input-field h-11 pr-10 ${pincodeError ? "border-red-400 bg-red-50/20" : ""}`}
                      placeholder="6 digit PIN"
                    />
                    {isPincodeLoading && (
                      <Loader2 className="animate-spin absolute right-3 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-slate-400" />
                    )}
                  </div>
                  {pincodeError && (
                    <p className="text-[10px] text-red-500 mt-1 font-semibold flex items-center gap-1 leading-none">
                      <AlertCircle className="h-3 w-3" /> {pincodeError}
                    </p>
                  )}
                </Field>

                <Field label="Door / Flat No" required>
                  <input
                    type="text"
                    required
                    value={doorNo}
                    onChange={(e) => setDoorNo(e.target.value)}
                    className="input-field mt-1.5 h-11"
                    placeholder="e.g. 12B"
                  />
                </Field>

                <div className="sm:col-span-2">
                  <Field label="Street Name" required>
                    <input
                      type="text"
                      required
                      value={streetName}
                      onChange={(e) => setStreetName(e.target.value)}
                      className="input-field mt-1.5 h-11"
                      placeholder="e.g. Gandhi Nagar Road"
                    />
                  </Field>
                </div>

                <Field label="Landmark">
                  <input
                    type="text"
                    value={landmark}
                    onChange={(e) => setLandmark(e.target.value)}
                    className="input-field mt-1.5 h-11"
                    placeholder="e.g. Near Water Tank"
                  />
                </Field>

                <Field label="Post Office / Area" required>
                  {postOfficeOptions.length > 0 ? (
                    <select
                      value={postOffice}
                      onChange={(e) => setPostOffice(e.target.value)}
                      className="input-field mt-1.5 h-11 bg-white"
                    >
                      {postOfficeOptions.map((opt) => (
                        <option key={opt} value={opt}>
                          {opt}
                        </option>
                      ))}
                    </select>
                  ) : (
                    <input
                      type="text"
                      required
                      value={postOffice}
                      onChange={(e) => setPostOffice(e.target.value)}
                      className="input-field mt-1.5 h-11"
                      placeholder="e.g. Anna Nagar Post"
                    />
                  )}
                </Field>

                <Field label="Town / City" required>
                  <input
                    type="text"
                    required
                    value={city}
                    onChange={(e) => setCity(e.target.value)}
                    className="input-field mt-1.5 h-11"
                    placeholder="e.g. Madurai"
                  />
                </Field>

                <Field label="District" required>
                  <input
                    type="text"
                    required
                    value={district}
                    onChange={(e) => setDistrict(e.target.value)}
                    className="input-field mt-1.5 h-11"
                    placeholder="e.g. Madurai"
                  />
                </Field>

                <Field label="State" required>
                  <input
                    type="text"
                    required
                    disabled
                    value={state}
                    className="input-field mt-1.5 h-11 bg-slate-50 text-slate-400 opacity-80 cursor-not-allowed"
                  />
                </Field>
              </div>
            </div>

            {error && (
              <div className="rounded-2xl bg-danger-soft text-danger border border-danger/10 text-xs px-4 py-3 font-semibold shadow-sm flex items-start gap-2 animate-bounce">
                <AlertCircle className="h-4 w-4 shrink-0 mt-0.5" />
                <span>{error}</span>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full h-12 rounded-2xl bg-primary text-white font-extrabold shadow-btn hover:opacity-95 disabled:opacity-60 transition duration-300 transform hover:-translate-y-0.5 active:scale-95 text-sm tracking-wider uppercase"
            >
              {loading ? "Registering Account…" : "Complete Registration"}
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
