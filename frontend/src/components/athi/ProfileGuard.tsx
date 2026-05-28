import React, { useState, useEffect } from "react";
import { ShieldCheck, User, Landmark, Users, ClipboardList, HelpCircle, CheckCircle, AlertCircle, Loader2 } from "lucide-react";
import { api, apiError } from "../../lib/api";
import { useAuth } from "../../lib/auth";
import { toast } from "sonner";
import verhoeff from "verhoeff";

export interface ProfileData {
  profile_completion: number;
  is_verified: boolean;
  aadhaar_verified: boolean;
  bank_verified: boolean;
  full_name: string;
  gender: string | null;
  dob: string | null;
  email: string | null;
  phone_number: string | null;
  profession: string | null;
  state: string | null;
  district: string | null;
  pincode: string | null;
  door_no: string | null;
  street_name: string | null;
  landmark: string | null;
  post_office: string | null;
  city: string | null;
  masked_aadhaar: string | null;
  account_number_masked: string | null;
  ifsc_code: string | null;
  bank_name: string | null;
  nominee_name: string | null;
  nominee_relationship: string | null;
  nominee_phone: string | null;
  nominee_door_no: string | null;
  nominee_street_name: string | null;
  nominee_landmark: string | null;
  nominee_post_office: string | null;
  nominee_city: string | null;
  nominee_district: string | null;
  nominee_state: string | null;
  nominee_pincode: string | null;
}

export function ProfileGuard({ children }: { children: React.ReactNode }) {
  const { signOut } = useAuth();
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form Fields
  const [gender, setGender] = useState("");
  const [dob, setDob] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [profession, setProfession] = useState("");
  
  // Aadhaar States
  const [aadhaar, setAadhaar] = useState("");
  const [aadhaarVerified, setAadhaarVerified] = useState<boolean | null>(null);
  const [aadhaarError, setAadhaarError] = useState<string | null>(null);

  // Address States
  const [state, setState] = useState("Tamil Nadu");
  const [district, setDistrict] = useState("");
  const [pincode, setPincode] = useState("");
  const [doorNo, setDoorNo] = useState("");
  const [streetName, setStreetName] = useState("");
  const [landmark, setLandmark] = useState("");
  const [postOffice, setPostOffice] = useState("");
  const [city, setCity] = useState("");

  // Pincode API States
  const [isPincodeLoading, setIsPincodeLoading] = useState(false);
  const [postOfficeOptions, setPostOfficeOptions] = useState<string[]>([]);
  const [pincodeError, setPincodeError] = useState<string | null>(null);

  // Bank & Nominee States
  const [bankName, setBankName] = useState("");
  const [accountNumber, setAccountNumber] = useState("");
  const [ifscCode, setIfscCode] = useState("");
  const [nomineeName, setNomineeName] = useState("");
  const [nomineeRelationship, setNomineeRelationship] = useState("");
  const [nomineePhone, setNomineePhone] = useState("");

  const [acceptRulesCheck, setAcceptRulesCheck] = useState(false);

  // Live Aadhaar Checksum verification
  useEffect(() => {
    if (aadhaar.length === 12) {
      if (aadhaar.includes("X")) {
        setAadhaarVerified(true);
        setAadhaarError(null);
      } else if (/^\d+$/.test(aadhaar) && verhoeff.validate(aadhaar)) {
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

  // Pincode Auto-Fill Address API Integration using Backend Proxy Route
  useEffect(() => {
    const fetchPincodeAddress = async () => {
      if (pincode.length === 6 && /^\d+$/.test(pincode)) {
        setIsPincodeLoading(true);
        setPincodeError(null);
        try {
          // Fetch via CORS-safe Backend Proxy API
          const { data } = await api.get(`/location/pincode/${pincode}`);
          if (data && data.success) {
            setState(data.state || "Tamil Nadu");
            setDistrict(data.district || "");
            setCity(data.city || "");
            
            if (data.post_office) {
              setPostOfficeOptions([data.post_office]);
              setPostOffice(data.post_office);
            }
            toast.success("Profile address details pre-filled successfully!");
          } else {
            setPincodeError(data.message || "Invalid Pincode or no records found.");
          }
        } catch (e) {
          console.error("Pincode API failed", e);
          setPincodeError("Unable to query location registry. Please type manually.");
        } finally {
          setIsPincodeLoading(false);
        }
      } else {
        setPostOfficeOptions([]);
      }
    };

    fetchPincodeAddress();
  }, [pincode]);

  const fetchProfile = async () => {
    try {
      const { data } = await api.get("/profiles/me");
      setProfile(data);
      
      // Preload form inputs if they already exist
      if (data) {
        setGender(data.gender || "");
        setDob(data.dob || "");
        setEmail(data.email || "");
        setPhone(data.phone_number || "");
        setProfession(data.profession || "");
        setState(data.state || "Tamil Nadu");
        setDistrict(data.district || "");
        setPincode(data.pincode || "");
        setDoorNo(data.door_no || "");
        setStreetName(data.street_name || "");
        setLandmark(data.landmark || "");
        setPostOffice(data.post_office || "");
        setCity(data.city || "");
        setBankName(data.bank_name || "");
        setIfscCode(data.ifsc_code || "");
        setNomineeName(data.nominee_name || "");
        setNomineeRelationship(data.nominee_relationship || "");
        setNomineePhone(data.nominee_phone || "");

        if (data.masked_aadhaar) {
          setAadhaar(data.masked_aadhaar);
          setAadhaarVerified(true);
        }
      }
    } catch (err) {
      toast.error("Unable to load profile completion configurations.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setUpdating(true);

    // Form validations
    if (aadhaarError) {
      setError("Please fix the Aadhaar card checksum error.");
      setUpdating(false);
      return;
    }

    if (pincode && (pincode.length !== 6 || !/^\d+$/.test(pincode))) {
      setError("Pincode must consist of exactly 6 numeric digits.");
      setUpdating(false);
      return;
    }

    if (nomineePhone && (nomineePhone.length !== 10 || !/^\d+$/.test(nomineePhone))) {
      setError("Nominee phone must consist of exactly 10 numeric digits.");
      setUpdating(false);
      return;
    }

    if (ifscCode && ifscCode.length !== 11) {
      setError("IFSC code must be exactly 11 characters.");
      setUpdating(false);
      return;
    }

    try {
      const payload: any = {
        gender: gender || null,
        dob: dob || null,
        email: email || null,
        profession: profession || null,
        state: state || null,
        district: district || null,
        pincode: pincode || null,
        door_no: doorNo || null,
        street_name: streetName || null,
        landmark: landmark || null,
        post_office: postOffice || null,
        city: city || null,
        bank_name: bankName || null,
        ifsc_code: ifscCode.toUpperCase() || null,
        nominee_name: nomineeName || null,
        nominee_relationship: nomineeRelationship || null,
        nominee_phone: nomineePhone || null,
      };

      if (aadhaar && !aadhaar.includes("X")) {
        payload.aadhaar = aadhaar;
      }

      if (accountNumber) {
        payload.account_number = accountNumber;
      }

      await api.put("/profiles/me", payload);
      toast.success("Profile details updated successfully!");
      fetchProfile();
    } catch (err) {
      setError(apiError(err));
    } finally {
      setUpdating(false);
    }
  };

  const handleAcceptRules = async () => {
    if (!acceptRulesCheck) return;
    setUpdating(true);
    try {
      await api.post("/profiles/me/accept-rules", {
        rules_version: "v1.0",
      });
      toast.success("Platform rules accepted successfully! Access Unlocked.");
      fetchProfile();
    } catch (err) {
      toast.error(apiError(err));
    } finally {
      setUpdating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-900 text-white text-sm font-medium">
        <Loader2 className="animate-spin h-5 w-5 mr-2 text-primary" /> Loading Profile Milestones…
      </div>
    );
  }

  // Auto bypass the guard if completed and click-wrap accepted inside DB
  if (profile && profile.profile_completion === 100 && profile.is_verified) {
    return <>{children}</>;
  }

  return (
    <div className="min-h-screen bg-slate-950/70 backdrop-blur-md flex items-center justify-center p-4 sm:p-6 overflow-y-auto">
      <div className="max-w-4xl w-full bg-white/95 backdrop-blur border border-slate-200/80 rounded-3xl shadow-modal overflow-hidden my-8 gov-tricolor-bar animate-fade-in-up">
        {/* Banner with Saffron/navy tricolor */}
        <div className="bg-gradient-to-br from-deep-blue to-primary text-white p-6 sm:p-8 relative">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white/15 backdrop-blur border border-white/10 shadow-sm">
                <ShieldCheck className="h-6 w-6" />
              </div>
              <span className="font-extrabold text-sm tracking-tight uppercase">Athiyaman Digital India</span>
            </div>
            
            <button
              onClick={signOut}
              className="px-4 py-2 rounded-xl bg-white/10 border border-white/20 text-xs font-black uppercase hover:bg-white/20 transition"
            >
              Sign Out
            </button>
          </div>

          <h2 className="mt-6 text-2xl sm:text-3xl font-extrabold tracking-tight">
            Profile Verification Guard Locked 🇮🇳
          </h2>
          <p className="mt-2 text-xs text-white/80 max-w-xl leading-relaxed">
            Under Swachh Bharat guidelines, you must complete your profile to **exactly 100%** (submitting biographical, physical address, verified Aadhaar, bank details, and nominee details) before unlocking dashboard actions.
          </p>

          <div className="absolute right-8 bottom-6 hidden md:block">
            <div className="relative flex items-center justify-center">
              <svg className="w-16 h-16 transform -rotate-90">
                <circle cx="32" cy="32" r="28" className="text-white/15" strokeWidth="6" fill="transparent" />
                <circle
                  cx="32"
                  cy="32"
                  r="28"
                  className="text-amber-400 transition-all duration-700"
                  strokeWidth="6"
                  fill="transparent"
                  strokeDasharray={2 * Math.PI * 28}
                  strokeDashoffset={2 * Math.PI * 28 * (1 - (profile?.profile_completion || 0) / 100)}
                />
              </svg>
              <span className="absolute text-sm font-black text-amber-300">{profile?.profile_completion || 0}%</span>
            </div>
          </div>
        </div>

        {/* Progress Bar (Mobile) */}
        <div className="md:hidden h-2 bg-slate-200 relative">
          <div
            className="h-full bg-amber-400 transition-all duration-500"
            style={{ width: `${profile?.profile_completion || 0}%` }}
          />
        </div>

        {/* Body forms */}
        <div className="p-6 sm:p-8">
          {profile && profile.profile_completion < 100 ? (
            <form onSubmit={handleUpdate} className="space-y-8">
              
              {/* Biographical Details */}
              <div>
                <h3 className="text-base font-bold text-slate-800 flex items-center gap-2 border-b border-slate-100 pb-2">
                  <User className="h-4.5 w-4.5 text-primary" /> 1. Citizen Biography
                </h3>
                <div className="mt-4 grid sm:grid-cols-3 gap-4">
                  <Field label="Full Name" required>
                    <input
                      type="text"
                      disabled
                      value={profile.full_name}
                      className="input-field mt-1.5 h-11 bg-slate-100 text-slate-400 opacity-80 cursor-not-allowed"
                    />
                  </Field>

                  <Field label="Email Address" required>
                    <input
                      type="email"
                      required
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="input-field mt-1.5 h-11"
                      placeholder="Enter email address"
                    />
                  </Field>

                  <Field label="Phone Number" required>
                    <input
                      type="text"
                      required
                      disabled={profile.phone_number ? true : false}
                      value={phone}
                      onChange={(e) => setPhone(e.target.value.replace(/\D/g, ""))}
                      className={`input-field mt-1.5 h-11 ${profile.phone_number ? "bg-slate-100 text-slate-400 opacity-80 cursor-not-allowed" : ""}`}
                      placeholder="10 digit phone number"
                    />
                  </Field>

                  <Field label="Gender" required>
                    <select
                      value={gender}
                      onChange={(e) => setGender(e.target.value)}
                      className="input-field mt-1.5 h-11"
                      required
                    >
                      <option value="">Select Gender</option>
                      <option value="MALE">Male</option>
                      <option value="FEMALE">Female</option>
                      <option value="OTHER">Other</option>
                    </select>
                  </Field>

                  <Field label="Date of Birth" required>
                    <input
                      type="date"
                      required
                      value={dob}
                      onChange={(e) => setDob(e.target.value)}
                      className="input-field mt-1.5 h-11"
                    />
                  </Field>

                  <Field label="Profession" required>
                    <input
                      type="text"
                      required
                      value={profession}
                      onChange={(e) => setProfession(e.target.value)}
                      className="input-field mt-1.5 h-11"
                      placeholder="e.g. Citizen, Farmer, Agent"
                    />
                  </Field>
                </div>
              </div>

              {/* Aadhaar Verification */}
              <div>
                <h3 className="text-base font-bold text-slate-800 flex items-center gap-2 border-b border-slate-100 pb-2">
                  <ShieldCheck className="h-4.5 w-4.5 text-primary" /> 2. Aadhaar Card Verification
                </h3>
                <div className="mt-4 max-w-md">
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

              {/* Physical Address */}
              <div>
                <h3 className="text-base font-bold text-slate-800 flex items-center gap-2 border-b border-slate-100 pb-2">
                  <ClipboardList className="h-4.5 w-4.5 text-primary" /> 3. Address Details (Indian PIN Auto-Fill)
                </h3>
                <div className="mt-4 grid sm:grid-cols-4 gap-4">
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
                        <span className="absolute right-3 top-1/2 -translate-y-1/2">
                          <Loader2 className="animate-spin h-4.5 w-4.5 text-slate-400" />
                        </span>
                      )}
                    </div>
                    {pincodeError && (
                      <p className="text-xs text-red-500 mt-1 font-semibold flex items-center gap-1">
                        <AlertCircle className="h-3.5 w-3.5" /> {pincodeError}
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
                      placeholder="e.g. 104-A"
                    />
                  </Field>

                  <div className="sm:col-span-2">
                    <Field label="Street / Colony" required>
                      <input
                        type="text"
                        required
                        value={streetName}
                        onChange={(e) => setStreetName(e.target.value)}
                        className="input-field mt-1.5 h-11"
                        placeholder="e.g. Nehru Nagar Colony"
                      />
                    </Field>
                  </div>

                  <Field label="Landmark">
                    <input
                      type="text"
                      value={landmark}
                      onChange={(e) => setLandmark(e.target.value)}
                      className="input-field mt-1.5 h-11"
                      placeholder="e.g. Opposite Park"
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
                        placeholder="e.g. Anna Road Post"
                      />
                    )}
                  </Field>

                  <Field label="City / Town" required>
                    <input
                      type="text"
                      required
                      value={city}
                      onChange={(e) => setCity(e.target.value)}
                      className="input-field mt-1.5 h-11"
                      placeholder="City/Town name"
                    />
                  </Field>

                  <Field label="District" required>
                    <input
                      type="text"
                      required
                      value={district}
                      onChange={(e) => setDistrict(e.target.value)}
                      className="input-field mt-1.5 h-11"
                      placeholder="District"
                    />
                  </Field>

                  <Field label="State" required>
                    <input
                      type="text"
                      required
                      disabled
                      value={state}
                      className="input-field mt-1.5 h-11 bg-slate-100 text-slate-400 opacity-80 cursor-not-allowed"
                    />
                  </Field>
                </div>
              </div>

              {/* Bank Details */}
              <div>
                <h3 className="text-base font-bold text-slate-800 flex items-center gap-2 border-b border-slate-100 pb-2">
                  <Landmark className="h-4.5 w-4.5 text-primary" /> 4. Banking Details (For Reward Payouts)
                </h3>
                <div className="mt-4 grid sm:grid-cols-3 gap-4">
                  <Field label="Bank Name" required>
                    <input
                      type="text"
                      required
                      value={bankName}
                      onChange={(e) => setBankName(e.target.value)}
                      className="input-field mt-1.5 h-11"
                      placeholder="e.g. State Bank of India"
                    />
                  </Field>

                  <Field label="Account Number" required>
                    <input
                      type="password"
                      required={!profile.account_number_masked}
                      value={accountNumber}
                      onChange={(e) => setAccountNumber(e.target.value.replace(/\D/g, ""))}
                      className="input-field mt-1.5 h-11"
                      placeholder={profile.account_number_masked ? `Masked: ${profile.account_number_masked}` : "Enter account number"}
                    />
                  </Field>

                  <Field label="IFSC Code" required>
                    <input
                      type="text"
                      required
                      maxLength={11}
                      value={ifscCode}
                      onChange={(e) => setIfscCode(e.target.value.toUpperCase())}
                      className="input-field mt-1.5 h-11 font-mono tracking-wider"
                      placeholder="e.g. SBIN0001234"
                    />
                  </Field>
                </div>
              </div>

              {/* Nominee Details */}
              <div>
                <h3 className="text-base font-bold text-slate-800 flex items-center gap-2 border-b border-slate-100 pb-2">
                  <Users className="h-4.5 w-4.5 text-primary" /> 5. Nominee Information
                </h3>
                <div className="mt-4 grid sm:grid-cols-3 gap-4">
                  <Field label="Nominee Name" required>
                    <input
                      type="text"
                      required
                      value={nomineeName}
                      onChange={(e) => setNomineeName(e.target.value)}
                      className="input-field mt-1.5 h-11"
                      placeholder="Enter nominee name"
                    />
                  </Field>

                  <Field label="Relationship" required>
                    <input
                      type="text"
                      required
                      value={nomineeRelationship}
                      onChange={(e) => setNomineeRelationship(e.target.value)}
                      className="input-field mt-1.5 h-11"
                      placeholder="e.g. Spouse, Parent"
                    />
                  </Field>

                  <Field label="Nominee Phone" required>
                    <input
                      type="text"
                      required
                      maxLength={10}
                      value={nomineePhone}
                      onChange={(e) => setNomineePhone(e.target.value.replace(/\D/g, ""))}
                      className="input-field mt-1.5 h-11"
                      placeholder="10 digit phone"
                    />
                  </Field>
                </div>
              </div>

              {error && (
                <div className="rounded-xl bg-danger-soft text-danger border border-danger/10 text-xs px-4 py-3 font-semibold shadow-sm flex items-start gap-2">
                  <AlertCircle className="h-4 w-4 shrink-0 mt-0.5" />
                  <span>{error}</span>
                </div>
              )}

              <div className="flex justify-end pt-4 border-t border-slate-100">
                <button
                  type="submit"
                  disabled={updating}
                  className="w-full sm:w-auto h-12 px-8 flex items-center justify-center rounded-xl bg-primary text-white font-extrabold shadow-btn hover:opacity-95 disabled:opacity-60 transition"
                >
                  {updating ? "Saving Progress…" : "Save Progress & Check Completeness"}
                </button>
              </div>
            </form>
          ) : (
            /* Rules Acceptance view when profile completion reaches exactly 100% */
            <div className="text-center py-6 animate-fade-in-up">
              <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-success-soft text-success shadow-btn animate-float">
                <CheckCircle className="h-8 w-8" />
              </div>
              <h3 className="mt-6 text-2xl font-extrabold text-slate-800 tracking-tight">Profile 100% Completed!</h3>
              <p className="mt-2 text-sm text-slate-500">
                Your biographical, geocoded address, and bank payout records are verified.
              </p>

              <div className="mt-8 max-w-xl mx-auto border border-slate-200 rounded-2xl bg-slate-50 p-6 text-left text-xs leading-relaxed space-y-3 shadow-inner">
                <p className="font-extrabold text-slate-800 text-sm flex items-center gap-1.5">
                  📜 Swachh Bharat Platform click-wrap legal rules (v1.0)
                </p>
                <p className="text-slate-500 font-medium">
                  By clicking accept, you acknowledge and agree that:
                </p>
                <ul className="list-disc pl-5 space-y-1.5 text-slate-600 font-semibold">
                  <li>Waste logs must consist strictly of physical resource collections backed with valid photo proof.</li>
                  <li>Filing fraudulent claims or duplicate payouts violates core directives and triggers account suspension.</li>
                  <li>Audit logs permanently document physical IP addresses and credentials traces for absolute transparency.</li>
                </ul>

                <label className="flex items-start gap-2.5 pt-4 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={acceptRulesCheck}
                    onChange={(e) => setAcceptRulesCheck(e.target.checked)}
                    className="mt-0.5 rounded text-primary focus:ring-primary h-4.5 w-4.5 cursor-pointer accent-primary"
                  />
                  <span className="text-xs font-bold text-slate-700">
                    I read, understood, and accept all the platform agreements and rules of the Athiyaman Platform.
                  </span>
                </label>
              </div>

              <div className="mt-8 flex justify-center gap-3">
                <button
                  onClick={handleAcceptRules}
                  disabled={updating || !acceptRulesCheck}
                  className="w-full max-w-xs h-12 flex items-center justify-center rounded-xl bg-success text-white font-extrabold shadow-btn hover:opacity-95 disabled:opacity-60 transition"
                >
                  {updating ? "Unlocking Account…" : "Accept Agreements & Unlock Dashboard"}
                </button>
              </div>
            </div>
          )}
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
