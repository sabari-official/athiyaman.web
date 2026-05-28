import React, { useState, useEffect } from "react";
import { ShieldCheck, User, Landmark, Users, ClipboardList, HelpCircle, CheckCircle } from "lucide-react";
import { api, apiError } from "../../lib/api";
import { toast } from "sonner";

export interface ProfileData {
  profile_completion: number;
  aadhaar_verified: boolean;
  bank_verified: boolean;
  full_name: string;
  gender: string | null;
  dob: string | null;
  email: string | null;
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
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [loading, setLoading] = useState(true);
  const [rulesAccepted, setRulesAccepted] = useState(false);
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form Fields
  const [gender, setGender] = useState("");
  const [dob, setDob] = useState("");
  const [email, setEmail] = useState("");
  const [profession, setProfession] = useState("");
  
  const [state, setState] = useState("Tamil Nadu");
  const [district, setDistrict] = useState("");
  const [pincode, setPincode] = useState("");
  const [doorNo, setDoorNo] = useState("");
  const [streetName, setStreetName] = useState("");
  const [landmark, setLandmark] = useState("");
  const [postOffice, setPostOffice] = useState("");
  const [city, setCity] = useState("");

  // Pincode API States for Profile Completion Guard
  const [isPincodeLoading, setIsPincodeLoading] = useState(false);
  const [postOfficeOptions, setPostOfficeOptions] = useState<string[]>([]);

  // Pincode Auto-Fill Address API Integration
  useEffect(() => {
    const fetchPincodeAddress = async () => {
      if (pincode.length === 6 && /^\d+$/.test(pincode)) {
        setIsPincodeLoading(true);
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
              if (!postOffice || !options.includes(postOffice)) {
                setPostOffice(options[0]);
              }
              toast.success("Profile address pre-filled from pincode successfully!");
            }
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

  const [bankName, setBankName] = useState("");
  const [accountNumber, setAccountNumber] = useState("");
  const [ifscCode, setIfscCode] = useState("");

  const [nomineeName, setNomineeName] = useState("");
  const [nomineeRelationship, setNomineeRelationship] = useState("");
  const [nomineePhone, setNomineePhone] = useState("");
  const [nomineeDoorNo, setNomineeDoorNo] = useState("");
  const [nomineeStreetName, setNomineeStreetName] = useState("");
  const [nomineeLandmark, setNomineeLandmark] = useState("");
  const [nomineePostOffice, setNomineePostOffice] = useState("");
  const [nomineeCity, setNomineeCity] = useState("");
  const [nomineeDistrict, setNomineeDistrict] = useState("");
  const [nomineeState, setNomineeState] = useState("Tamil Nadu");
  const [nomineePincode, setNomineePincode] = useState("");

  const [acceptRulesCheck, setAcceptRulesCheck] = useState(false);

  const fetchProfile = async () => {
    try {
      const { data } = await api.get("/profiles/me");
      setProfile(data);
      
      // Preload form inputs if they already exist
      if (data) {
        setGender(data.gender || "");
        setDob(data.dob || "");
        setEmail(data.email || "");
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
        setNomineeDoorNo(data.nominee_door_no || "");
        setNomineeStreetName(data.nominee_street_name || "");
        setNomineeLandmark(data.nominee_landmark || "");
        setNomineePostOffice(data.nominee_post_office || "");
        setNomineeCity(data.nominee_city || "");
        setNomineeDistrict(data.nominee_district || "");
        setNomineeState(data.nominee_state || "Tamil Nadu");
        setNomineePincode(data.nominee_pincode || "");
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

    // Minor validation checks
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
        nominee_door_no: nomineeDoorNo || null,
        nominee_street_name: nomineeStreetName || null,
        nominee_landmark: nomineeLandmark || null,
        nominee_post_office: nomineePostOffice || null,
        nominee_city: nomineeCity || null,
        nominee_district: nomineeDistrict || null,
        nominee_state: nomineeState || null,
        nominee_pincode: nomineePincode || null,
      };

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
      toast.success("Platform click-wrap legal rules accepted successfully! Access Unlocked.");
      setRulesAccepted(true);
      fetchProfile();
    } catch (err) {
      toast.error(apiError(err));
    } finally {
      setUpdating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background text-muted-foreground text-sm font-medium">
        Loading Profile Milestones…
      </div>
    );
  }

  // If profile is fully complete and rules accepted, release the dashboard
  if (profile && profile.profile_completion === 100) {
    // If rules acceptance is already complete inside DB, release
    return <>{children}</>;
  }

  return (
    <div className="min-h-screen bg-slate-900/50 backdrop-blur-md flex items-center justify-center p-4 sm:p-6 overflow-y-auto">
      <div className="max-w-4xl w-full bg-card border border-border rounded-3xl shadow-modal overflow-hidden my-8">
        {/* Banner */}
        <div className="bg-nav-gradient text-white p-6 sm:p-8 relative">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white/15 backdrop-blur">
              <ShieldCheck className="h-6 w-6" />
            </div>
            <span className="font-extrabold text-sm tracking-tight">Athiyaman Digital India</span>
          </div>

          <h2 className="mt-6 text-2xl sm:text-3xl font-extrabold tracking-tight">
            Profile Completion Guard Locked
          </h2>
          <p className="mt-2 text-sm text-white/85 max-w-xl leading-relaxed">
            Under Swachh Bharat guidelines, you must complete your profile to **exactly 100%** (submitting biographical, address, bank payout records, and nominee details) before unlocking dashboard actions.
          </p>

          <div className="absolute right-6 bottom-6 hidden md:block">
            <div className="relative flex items-center justify-center">
              <svg className="w-16 h-16 transform -rotate-90">
                <circle cx="32" cy="32" r="28" className="text-white/15" strokeWidth="6" fill="transparent" />
                <circle
                  cx="32"
                  cy="32"
                  r="28"
                  className="text-success"
                  strokeWidth="6"
                  fill="transparent"
                  strokeDasharray={2 * Math.PI * 28}
                  strokeDashoffset={2 * Math.PI * 28 * (1 - (profile?.profile_completion || 0) / 100)}
                />
              </svg>
              <span className="absolute text-sm font-extrabold">{profile?.profile_completion || 0}%</span>
            </div>
          </div>
        </div>

        {/* Progress Bar (Mobile) */}
        <div className="md:hidden h-2.5 bg-muted relative">
          <div
            className="h-full bg-success transition-all duration-500"
            style={{ width: `${profile?.profile_completion || 0}%` }}
          />
        </div>

        {/* Body forms */}
        <div className="p-6 sm:p-8">
          {profile && profile.profile_completion < 100 ? (
            <form onSubmit={handleUpdate} className="space-y-8">
              {/* Biographical Details */}
              <div>
                <h3 className="text-base font-bold text-foreground flex items-center gap-2 border-b border-border pb-2">
                  <User className="h-4.5 w-4.5 text-primary" /> 1. Citizen Biography
                </h3>
                <div className="mt-4 grid sm:grid-cols-4 gap-4">
                  <Field label="Full Name" required>
                    <input
                      type="text"
                      disabled
                      value={profile.full_name}
                      className="input-field mt-1.5 h-11 bg-muted text-muted-foreground opacity-80"
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
                      placeholder="e.g. Citizen, Farmer"
                    />
                  </Field>
                </div>
              </div>

              {/* Physical Address */}
              <div>
                <h3 className="text-base font-bold text-foreground flex items-center gap-2 border-b border-border pb-2">
                  <ClipboardList className="h-4.5 w-4.5 text-primary" /> 2. Address Details
                </h3>
                <div className="mt-4 grid sm:grid-cols-4 gap-4">
                  <Field label="Door No" required>
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
                      placeholder="e.g. Opposite Post Office"
                    />
                  </Field>

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
                        <span className="absolute right-3 top-1/2 -translate-y-1/2">
                          <svg className="animate-spin h-4.5 w-4.5 text-slate-400" viewBox="0 0 24 24" fill="none">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                          </svg>
                        </span>
                      )}
                    </div>
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

                  <Field label="City" required>
                    <input
                      type="text"
                      required
                      value={city}
                      onChange={(e) => setCity(e.target.value)}
                      className="input-field mt-1.5 h-11"
                      placeholder="e.g. Chennai"
                    />
                  </Field>

                  <Field label="District" required>
                    <input
                      type="text"
                      required
                      value={district}
                      onChange={(e) => setDistrict(e.target.value)}
                      className="input-field mt-1.5 h-11"
                      placeholder="e.g. Chennai"
                    />
                  </Field>
                </div>
              </div>

              {/* Bank Details */}
              <div>
                <h3 className="text-base font-bold text-foreground flex items-center gap-2 border-b border-border pb-2">
                  <Landmark className="h-4.5 w-4.5 text-primary" /> 3. Banking Details (For Reward Disbursements)
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
                <h3 className="text-base font-bold text-foreground flex items-center gap-2 border-b border-border pb-2">
                  <Users className="h-4.5 w-4.5 text-primary" /> 4. Nominee Information
                </h3>
                <div className="mt-4 grid sm:grid-cols-4 gap-4">
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
                      placeholder="e.g. Spouse, Father"
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

                  <Field label="Nominee City" required>
                    <input
                      type="text"
                      required
                      value={nomineeCity}
                      onChange={(e) => setNomineeCity(e.target.value)}
                      className="input-field mt-1.5 h-11"
                      placeholder="City of nominee"
                    />
                  </Field>
                </div>
              </div>

              {error && (
                <div className="rounded-xl bg-danger-soft text-danger border border-danger/10 text-xs px-4 py-3 font-semibold">
                  ⚠️ {error}
                </div>
              )}

              <div className="flex justify-end pt-4 border-t border-border">
                <button
                  type="submit"
                  disabled={updating}
                  className="w-full sm:w-auto h-12 px-8 flex items-center justify-center rounded-xl bg-primary text-white font-bold shadow-btn hover:opacity-95 disabled:opacity-60 transition"
                >
                  {updating ? "Saving Progress…" : "Save Progress & Check Completeness"}
                </button>
              </div>
            </form>
          ) : (
            /* Rules Acceptance view when profile completion reaches exactly 100% */
            <div className="text-center py-6">
              <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-success-soft text-success shadow-btn">
                <CheckCircle className="h-8 w-8" />
              </div>
              <h3 className="mt-6 text-2xl font-extrabold text-foreground tracking-tight">Profile 100% Completed!</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                Your biographical, geocoded address, and bank payout records are verified.
              </p>

              <div className="mt-8 max-w-xl mx-auto border border-border rounded-2xl bg-muted p-5 text-left text-xs leading-relaxed space-y-3">
                <p className="font-bold text-foreground text-sm">📜 Platform Legal Rules click-wrap agreements (v1.0)</p>
                <p className="text-muted-foreground">
                  By clicking accept, you acknowledge and agree that:
                </p>
                <ul className="list-disc pl-5 space-y-1.5 text-muted-foreground">
                  <li>Waste logs must consist strictly of physical resource collections backed with valid photo proof.</li>
                  <li>Filing fraudulent claims or duplicate payouts violates core directives and triggers account suspension.</li>
                  <li>Audit logs permanently document physical IP addresses and credentials traces for absolute transparency.</li>
                </ul>

                <label className="flex items-start gap-2.5 pt-4 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={acceptRulesCheck}
                    onChange={(e) => setAcceptRulesCheck(e.target.checked)}
                    className="mt-0.5 rounded text-primary focus:ring-primary h-4.5 w-4.5 cursor-pointer"
                  />
                  <span className="text-xs font-semibold text-foreground">
                    I read, understood, and accept all the platform agreements and rules of the Athiyaman Platform.
                  </span>
                </label>
              </div>

              <div className="mt-8 flex justify-center gap-3">
                <button
                  onClick={handleAcceptRules}
                  disabled={updating || !acceptRulesCheck}
                  className="w-full max-w-xs h-12 flex items-center justify-center rounded-xl bg-success text-success-foreground font-bold shadow-btn hover:opacity-95 disabled:opacity-60 transition"
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
      <span className="text-xs font-bold text-foreground flex items-center gap-1">
        {label} {required && <span className="text-danger">*</span>}
      </span>
      {children}
    </label>
  );
}
