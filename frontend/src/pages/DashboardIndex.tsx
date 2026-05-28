import { useAuth } from "../lib/auth";
import { useTeamProgress, usePersonalProgress, useSubmitClaim } from "../lib/hooks";
import { StatCard } from "../components/athi/StatCard";
import { LevelTree } from "../components/athi/LevelTree";
import type { ProgressItem } from "../components/athi/LevelTree";
import { Recycle, Users, Award, Landmark, MapPin } from "lucide-react";

export function DashboardIndex() {
  const { user } = useAuth();
  
  // Fetch levels queries
  const { data: teamProgress, isLoading: loadingTeam } = useTeamProgress();
  const { data: personalProgress, isLoading: loadingPersonal } = usePersonalProgress();
  
  // Claim submit mutation
  const submitClaimMutation = useSubmitClaim();

  const handleClaim = (_levelId: string, levelNumber: number, _reward: number) => {
    submitClaimMutation.mutate({
      claim_type: levelNumber <= 6 ? "TEAM_REWARD" : "PERSONAL_REWARD",
      level_number: levelNumber,
      accept_rules: true,
    });
  };

  // Convert and combine relational DB progression arrays into the timeline items
  const teamItems: ProgressItem[] = (teamProgress || []).map((t) => ({
    id: t.id,
    level_number: t.level.level_number,
    level_type: "TEAM",
    requirement_type: t.level.requirement_type,
    requirement_value: t.level.requirement_value,
    reward_amount: t.level.reward_amount,
    status: t.status,
    progress_value: t.current_member_count,
  }));

  const personalItems: ProgressItem[] = (personalProgress || []).map((p) => ({
    id: p.id,
    level_number: p.level.level_number,
    level_type: "PERSONAL",
    requirement_type: p.level.requirement_type,
    requirement_value: p.level.requirement_value,
    reward_amount: p.level.reward_amount,
    status: p.status,
    progress_value: p.approved_waste_kg,
  }));

  const combinedLevels = [...teamItems, ...personalItems].sort(
    (a, b) => a.level_number - b.level_number
  );

  // Compute analytics summaries
  const activeTeamProgress = teamItems.find((t) => t.status === "IN_PROGRESS");
  const activePersonalProgress = personalItems.find((p) => p.status === "IN_PROGRESS");

  const completedTeamCount = teamItems.filter((t) => t.status === "COMPLETED" || t.status === "CLAIMED").length;
  const completedPersonalCount = personalItems.filter((p) => p.status === "COMPLETED" || p.status === "CLAIMED").length;
  
  const totalApprovedKg = personalItems.reduce((acc, p) => acc + p.progress_value, 0);
  const totalMembers = teamItems.length > 0 ? (teamProgress?.[0]?.current_member_count || 0) : 0;

  const currentLevelNumber =
    activePersonalProgress?.level_number ||
    activeTeamProgress?.level_number ||
    (completedPersonalCount > 0 ? 11 : completedTeamCount > 0 ? 6 : 1);

  if (loadingTeam || loadingPersonal) {
    return (
      <div className="flex h-64 items-center justify-center text-muted-foreground text-sm font-medium">
        Syncing Level Progression meters…
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-extrabold text-foreground tracking-tight">Citizen Dashboard</h1>
        <p className="mt-1.5 text-sm text-muted-foreground">
          Track your team recruitment milestones, upload verified collections, and claim milestone rewards.
        </p>
      </div>

      {/* Metric Cards grid */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Current Level"
          value={`L-${currentLevelNumber}`}
          sub={
            currentLevelNumber <= 6
              ? "Active: Team Roster Size"
              : "Active: Recycled Weight"
          }
          icon={<Award className="h-5 w-5" />}
          tone="primary"
        />

        <StatCard
          label="Total Approved Waste"
          value={`${totalApprovedKg.toFixed(1)} KG`}
          sub="Verified collection weight"
          icon={<Recycle className="h-5 w-5" />}
          tone="success"
        />

        {user?.role === "LEADER" ? (
          <StatCard
            label="Active Team Members"
            value={`${totalMembers} Citizens`}
            sub="Invite slot bounds"
            icon={<Users className="h-5 w-5" />}
            tone="primary"
          />
        ) : (
          <StatCard
            label="Invitation Status"
            value="Joined"
            sub="Affiliated with Active Team"
            icon={<Users className="h-5 w-5" />}
            tone="neutral"
          />
        )}

        <StatCard
          label="Completed Milestones"
          value={`${completedTeamCount + completedPersonalCount} / 11`}
          sub="Level rewards claims"
          icon={<Landmark className="h-5 w-5" />}
          tone="warning"
        />
      </div>

      {/* Main timeline & geolocator columns */}
      <div className="grid lg:grid-cols-3 gap-6 items-start">
        {/* Progress Timeline tree */}
        <div className="lg:col-span-2 space-y-6">
          <div className="card">
            <h2 className="text-lg font-bold text-foreground mb-4">Milestone Progress timeline</h2>
            <LevelTree levels={combinedLevels} onClaim={handleClaim} />
          </div>
        </div>

        {/* Sidebar geolocator */}
        <div className="space-y-6">
          <div className="rounded-2xl border border-border bg-card p-6 shadow-card">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-success-soft text-success mb-4">
              <MapPin className="h-5 w-5" />
            </div>
            <h3 className="text-base font-bold text-foreground">Find Collection Centers</h3>
            <p className="mt-2 text-xs text-muted-foreground leading-relaxed">
              Deposit your cleaned recyclable waste at nearest collection center. Provide your citizen **User ID** to Center Managers to log your weight.
            </p>

            <div className="mt-5 space-y-3">
              <div className="rounded-xl bg-muted p-3.5 border border-border">
                <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">
                  Your Account User ID
                </span>
                <p className="mt-1 font-mono text-xs text-foreground font-bold tracking-tight select-all">
                  {user?.user_id}
                </p>
              </div>

              <div className="text-xs space-y-2 border-t border-border pt-4">
                <p className="flex justify-between">
                  <span className="text-muted-foreground font-medium">📍 Madurai Center:</span>
                  <span className="font-bold text-foreground">Active (08:00 - 17:00)</span>
                </p>
                <p className="flex justify-between">
                  <span className="text-muted-foreground font-medium">📍 Chennai Center:</span>
                  <span className="font-bold text-foreground">Active (09:00 - 18:00)</span>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
export default DashboardIndex;
