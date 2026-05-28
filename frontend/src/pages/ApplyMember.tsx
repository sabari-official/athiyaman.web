import React, { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { ShieldCheck, User, Phone, Mail, MapPin, CheckCircle, Loader2 } from "lucide-react";
import verhoeff from "verhoeff";
import { api, apiError } from "../lib/api";
import { toast } from "sonner";

export function ApplyMember() {
  const navigate = useNavigate();
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form Fields
  const [fullName, setFullName] = useState("");
  const [phone, setPhone] = useState("");
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

  // Pincode API & Aadhaar Verification State
  const [isPincodeLoading, setIsPincodeLoading] = useState(false);
  const [postOfficeOptions, setPostOfficeOptions] = useState<string[]>([]);
  const [aadhaarVerified, setAadhaarVerified] = useState<boolean | null>(null);

  // Aadhaar Real-Time Verification Trigger
  useEffect(() => {
    if (aadhaar.length === 12) {
      if (/^\d+$/.test(aadhaar) && verhoeff.validate(aadhaar)) {
        setAadhaarVerified(true);
      } else {
        setAadhaarVerified(false);
      }
    } else {
      setAadhaarVerified(null);
    }
  }, [aadhaar]);

  // Pincode Auto-Fill Address API Integration
  useEffect(() => {
    const fetchPincodeAddress = async () => {
      if (pincode.length === 6 && /^\d+$/.test(pincode)) {
        setIsPincodeLoading(true);
        setError(null);
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
              setPostOffice(options[0]); // Select first post office by default
              toast.success("Address pre-filled from pincode successfully!");
            }
          } else {
            toast.error("Invalid Pincode or no records found.");
          }
        } catch (e) {
          console.error("Pincode API failed, falling back to manual entry", e);
        } finally {
          setIsPincodeLoading(false);
        }
      } else {
        setPostOfficeOptions([]);
      }
    };

    fetchPincodeAddress();
  }, [pincode]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // 1. Aadhaar length and Verhoeff validation check
    if (aadhaar.length !== 12 || !/^\d+$/.test(aadhaar)) {
      setError("Aadhaar number must consist of exactly 12 numeric digits.");
      return;
    }

    if (!verhoeff.validate(aadhaar)) {
      setError("Invalid Aadhaar number checksum. Verification failed.");
      return;
    }

    // 2. Phone number length validation check
    if (phone.length !== 10 || !/^\d+$/.test(phone)) {
      setError("Phone number must consist of exactly 10 digits.");
      return;
    }

    // 3. Pincode length check
    if (pincode.length !== 6 || !/^\d+$/.test(pincode)) {
      setError("Pincode must consist of exactly 6 digits.");
      return;
    }

    setLoading(true);
    try {
      // Endpoint: POST /api/v1/applications/member
      await api.post("/applications/member", {
        full_name: fullName,
        phone,
        email,
        aadhaar,
        state,
        district,
        pincode,
        door_no: doorNo,
        street_name: streetName,
        landmark: landmark || null,
        post_office: postOffice,
        city,
        reason: null, // Simple member form does not require reason
      });

      toast.success("Member application submitted successfully!");
      setSuccess(true);
    } catch (err) {
      setError(apiError(err));
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-6 relative">
        {/* Floating Glowing Lights */}
        <div className="absolute top-20 left-10 w-96 h-96 rounded-full bg-blue-300/10 blur-[80px] animate-pulse-glow pointer-events-none" />
        <div className="absolute bottom-20 right-10 w-96 h-96 rounded-full bg-emerald-300/10 blur-[80px] animate-pulse-glow pointer-events-none" />

        <div className="max-w-md w-full text-center bg-white/70 backdrop-blur-lg border border-white/50 p-8 rounded-3xl shadow-2xl relative animate-fade-in-up">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-emerald-50 text-success border border-emerald-100 shadow-btn animate-float">
            <CheckCircle className="h-8 w-8" />
          </div>
          <h2 className="mt-6 text-3xl font-black text-slate-800 tracking-tight">Application Submitted!</h2>
          <p className="mt-3 text-sm text-slate-600 leading-relaxed">
            Your application to join as a member has been filed successfully. Your local Team Leader will review details for your PIN code area and contact you with a direct registration link.
          </p>
          <div className="mt-8 space-y-3">
            <Link
              to="/"
              className="flex w-full h-12 items-center justify-center rounded-xl bg-primary text-white font-bold shadow-btn hover:opacity-95 transition"
            >
              Back to Home Screen
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background py-16 px-4 sm:px-6 relative overflow-hidden">
      {/* Decorative Auras */}
      <div className="absolute top-[-5%] left-[-5%] w-[450px] h-[450px] rounded-full bg-blue-400/5 blur-[90px] animate-pulse-glow pointer-events-none" />
      <div className="absolute bottom-[5%] right-[-5%] w-[450px] h-[450px] rounded-full bg-emerald-400/5 blur-[90px] animate-pulse-glow pointer-events-none" style={{ animationDelay: '-3s' }} />

      <div className="max-w-3xl mx-auto bg-white/80 backdrop-blur-md border border-white/50 rounded-3xl shadow-2xl overflow-hidden relative animate-fade-in-up">
        {/* Header banner */}
        <div className="bg-nav-gradient text-white p-8 relative overflow-hidden">
          <div className="absolute -right-16 -top-16 h-48 w-48 rounded-full bg-white/5" />
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white/15 backdrop-blur border border-white/10">
              <ShieldCheck className="h-6 w-6" />
            </div>
            <span className="font-extrabold text-lg tracking-tight">Athiyaman Digital India</span>
          </div>
          <h1 className="mt-6 text-3xl font-black tracking-tight">Join as a Platform Member</h1>
          <p className="mt-2 text-sm text-white/85 leading-relaxed max-w-xl">
            Register your verified details to participate under an approved Team Leader. Submit your physical address and Aadhaar to secure your community profile.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="p-8 space-y-8">
          {/* section 1: Bio */}
          <div className="space-y-4">
            <h3 className="text-base font-bold text-slate-800 flex items-center gap-2 border-b border-slate-100 pb-2">
              <User className="h-5 w-5 text-primary" /> Personal Information
            </h3>
            <div className="grid sm:grid-cols-2 gap-5">
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

              <Field label="Aadhaar Card Number" required>
                <div className="relative mt-1.5">
                  <input
                    type="text"
                    required
                    maxLength={12}
                    value={aadhaar}
                    onChange={(e) => setAadhaar(e.target.value.replace(/\D/g, ""))}
                    className={`input-field h-11 pr-24 ${
                      aadhaarVerified === true ? "border-emerald-500 bg-emerald-50/20" : aadhaarVerified === false ? "border-red-500 bg-red-50/20" : ""
                    }`}
                    placeholder="12 digit number"
                  />
                  {aadhaarVerified === true && (
                    <span className="absolute right-3 top-1/2 -translate-y-1/2 inline-flex items-center gap-1 text-[10px] font-black uppercase text-success px-2 py-0.5 rounded-full bg-success-soft border border-success/20 shadow-sm animate-float">
                      ✓ Verified
                    </span>
                  )}
                  {aadhaarVerified === false && (
                    <span className="absolute right-3 top-1/2 -translate-y-1/2 inline-flex items-center gap-1 text-[10px] font-black uppercase text-danger px-2 py-0.5 rounded-full bg-danger-soft border border-danger/20">
                      ✗ Invalid
                    </span>
                  )}
                </div>
                {aadhaarVerified === false && (
                  <p className="text-xs text-red-500 mt-1 font-semibold">Invalid Aadhaar number checksum. Check digits carefully.</p>
                )}
              </Field>

              <Field label="Phone Number" required>
                <div className="relative mt-1.5">
                  <Phone className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                  <input
                    type="text"
                    required
                    maxLength={10}
                    value={phone}
                    onChange={(e) => setPhone(e.target.value.replace(/\D/g, ""))}
                    className="input-field pl-9 h-11"
                    placeholder="10 digit mobile"
                  />
                </div>
              </Field>

              <Field label="Email Address" required>
                <div className="relative mt-1.5">
                  <Mail className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="input-field pl-9 h-11"
                    placeholder="you@example.com"
                  />
                </div>
              </Field>
            </div>
          </div>

          {/* section 2: Address */}
          <div className="space-y-4">
            <h3 className="text-base font-bold text-slate-800 flex items-center gap-2 border-b border-slate-100 pb-2">
              <MapPin className="h-5 w-5 text-primary" /> Physical Address
            </h3>
            <div className="grid sm:grid-cols-3 gap-5">
              <Field label="Pincode" required>
                <div className="relative mt-1.5">
                  <input
                    type="text"
                    required
                    maxLength={6}
                    value={pincode}
                    onChange={(e) => setPincode(e.target.value.replace(/\D/g, ""))}
                    className="input-field h-11 pr-10"
                    placeholder="6 digit pincode"
                  />
                  {isPincodeLoading && (
                    <Loader2 className="animate-spin absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                  )}
                </div>
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
                <Field label="Street / Colony Name" required>
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
            <div className="rounded-xl bg-danger-soft text-danger border border-danger/10 text-xs px-4 py-3 font-semibold shadow-sm">
              ⚠️ {error}
            </div>
          )}

          <div className="flex flex-col sm:flex-row items-center justify-end gap-3 pt-6 border-t border-slate-100">
            <Link
              to="/"
              className="w-full sm:w-auto h-12 px-6 flex items-center justify-center rounded-xl border border-slate-200 text-slate-500 hover:bg-slate-50 font-bold transition duration-300 text-sm"
            >
              Cancel
            </Link>
            <button
              type="submit"
              disabled={loading}
              className="w-full sm:w-auto h-12 px-8 flex items-center justify-center rounded-xl bg-primary text-white font-bold shadow-btn hover:opacity-95 disabled:opacity-60 transition duration-300 text-sm tracking-wide"
            >
              {loading ? "Filing Application…" : "Submit Registration"}
            </button>
          </div>
        </form>
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
