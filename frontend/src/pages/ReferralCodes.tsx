import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api, apiError } from "../lib/api";
import { toast } from "sonner";
import { Gift, Copy, ClipboardList, RefreshCw, Info, Lock } from "lucide-react";
import { fmtDate } from "../lib/format";

interface ReferralResponse {
  id: string;
  code: string;
  referral_type: string;
  team_id: string | null;
  level_number: number | null;
  max_usage: number;
  used_count: number;
  is_active: boolean;
  expires_at: string;
  created_at: string;
}

export function ReferralCodes() {
  const qc = useQueryClient();
  const [levelNumber, setLevelNumber] = useState(1);

  // Fetch current active referral code
  const { data: activeCode, isLoading, refetch } = useQuery({
    queryKey: ["current-referral"],
    queryFn: async () => {
      try {
        const { data } = await api.get("/api/v1/referrals/active");
        return data as ReferralResponse;
      } catch (err: any) {
        if (err.response?.status === 404) {
          return null; // Safe fallback if no code is active
        }
        throw err;
      }
    },
  });

  // Generate Referral Mutation matching our backend schemas exactly
  const generateMutation = useMutation({
    mutationFn: async (payload: { referral_type: "TEAM"; level_number: number }) => {
      const { data } = await api.post("/api/v1/referrals/", payload);
      return data as ReferralResponse;
    },
    onSuccess: (data) => {
      toast.success(`Success! Referral Code "${data.code}" generated.`);
      qc.invalidateQueries({ queryKey: ["current-referral"] });
    },
    onError: (err) => {
      toast.error(apiError(err));
    },
  });

  const handleGenerate = (e: React.FormEvent) => {
    e.preventDefault();
    generateMutation.mutate({
      referral_type: "TEAM",
      level_number: Number(levelNumber),
    });
  };

  const handleCopy = (code: string) => {
    navigator.clipboard.writeText(code);
    toast.success(`Copied "${code}" to clipboard!`);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-foreground tracking-tight flex items-center gap-2">
          <Gift className="h-6 w-6 text-primary" /> Team Referrals Management
        </h1>
        <p className="mt-1 text-xs text-muted-foreground">
          Recruit local citizens using structured team enrollment codes mapping to levels.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-6 items-start">
        {/* Active Code container */}
        <div className="md:col-span-2 space-y-6">
          <div className="card">
            <h2 className="text-base font-bold text-foreground mb-4 flex items-center gap-1.5">
              <ClipboardList className="h-4.5 w-4.5 text-primary" /> Active Invitation Code
            </h2>

            {isLoading ? (
              <div className="flex h-32 items-center justify-center text-muted-foreground text-xs font-semibold">
                Checking active referrals…
              </div>
            ) : !activeCode ? (
              <div className="flex flex-col items-center justify-center p-6 bg-slate-50 border border-dashed border-border rounded-2xl text-center">
                <span className="text-xl">🎟️</span>
                <p className="mt-2 text-sm font-semibold text-foreground">No Invitation Code Active</p>
                <p className="mt-1 text-xs text-muted-foreground max-w-sm">
                  You must generate an active referral code representing your current level target to invite new citizens to your group.
                </p>

                {/* Form to generate */}
                <form onSubmit={handleGenerate} className="mt-6 flex flex-col sm:flex-row items-end gap-3 w-full max-w-md">
                  <label className="block text-left flex-1">
                    <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest block">
                      Target Payout Milestone level
                    </span>
                    <select
                      value={levelNumber}
                      onChange={(e) => setLevelNumber(Number(e.target.value))}
                      className="input-field mt-1.5 h-11"
                    >
                      <option value="1">Team Level 1 (Milestone: 10 Members)</option>
                      <option value="2">Team Level 2 (Milestone: 90 Members)</option>
                      <option value="3">Team Level 3 (Milestone: 720 Members)</option>
                      <option value="4">Team Level 4 (Milestone: 5040 Members)</option>
                      <option value="5">Team Level 5 (Milestone: 30240 Members)</option>
                      <option value="6">Team Level 6 (Milestone: 50000 Members)</option>
                    </select>
                  </label>
                  <button
                    type="submit"
                    disabled={generateMutation.isPending}
                    className="h-11 px-5 rounded-xl bg-primary text-white text-xs font-bold hover:opacity-95 disabled:opacity-60 transition shrink-0"
                  >
                    {generateMutation.isPending ? "Generating…" : "Generate Code"}
                  </button>
                </form>
              </div>
            ) : (
              <div className="space-y-6">
                <div className="rounded-2xl border border-primary/10 bg-primary-soft/50 p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-6">
                  <div>
                    <span className="text-[10px] font-bold text-primary uppercase tracking-widest">
                      Active Shareable Code
                    </span>
                    <p className="mt-2 font-mono text-3xl font-extrabold text-foreground tracking-widest uppercase">
                      {activeCode.code}
                    </p>
                    <p className="mt-2 text-xs text-muted-foreground">
                      Expires: <span className="font-semibold text-foreground">{fmtDate(activeCode.expires_at)}</span>
                    </p>
                  </div>
                  <button
                    onClick={() => handleCopy(activeCode.code)}
                    className="h-11 px-5 flex items-center gap-1.5 rounded-xl bg-primary text-white text-xs font-bold hover:opacity-95 shadow-btn transition shrink-0"
                  >
                    <Copy className="h-4 w-4" /> Copy Code
                  </button>
                </div>

                {/* Quota details */}
                <div className="grid grid-cols-2 gap-4 border-t border-border pt-5 text-xs">
                  <div>
                    <p className="text-muted-foreground font-semibold">Active Milestone Level</p>
                    <p className="mt-1 font-bold text-foreground text-sm">Level {activeCode.level_number}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground font-semibold">Invite Usage Slots</p>
                    <p className="mt-1 font-bold text-foreground text-sm">
                      {activeCode.used_count} / {activeCode.max_usage} used
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Sidebar notes */}
        <div className="space-y-6">
          <div className="rounded-2xl border border-border bg-card p-5 shadow-card text-xs leading-relaxed space-y-3">
            <h3 className="font-bold text-foreground text-sm flex items-center gap-1.5">
              <Info className="h-4.5 w-4.5 text-primary" /> Invitation Rules
            </h3>
            <ul className="list-disc pl-4 space-y-2 text-muted-foreground">
              <li>Each code matches your team's active progression level.</li>
              <li>New members must input this code during registration to affiliate under your team name.</li>
              <li>Only one active invitation code is allowed per team. If you need to change targets, the active code must be fully utilized or expire to regenerate.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
export default ReferralCodes;
