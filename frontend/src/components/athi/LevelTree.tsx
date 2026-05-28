import { Lock, Check, Users, User, Sparkles } from "lucide-react";
import { fmtINR } from "../../lib/format";

export interface ProgressItem {
  id: string;
  level_number: number;
  level_type: "TEAM" | "PERSONAL";
  requirement_type: string;
  requirement_value: number;
  reward_amount: number;
  status: "LOCKED" | "IN_PROGRESS" | "COMPLETED" | "CLAIMED";
  progress_value: number;
}

function LevelCircle({ status, number }: { status: ProgressItem["status"]; number: number }) {
  if (status === "LOCKED")
    return (
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-muted text-muted-foreground border border-border">
        <Lock className="h-5 w-5" />
      </div>
    );
  if (status === "COMPLETED" || status === "CLAIMED")
    return (
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-success text-success-foreground shadow-btn">
        <Check className="h-6 w-6" />
      </div>
    );
  // IN_PROGRESS
  return (
    <div className="relative">
      <div className="absolute inset-0 rounded-full bg-primary/30 animate-ping" />
      <div className="relative flex h-12 w-12 items-center justify-center rounded-full bg-primary text-primary-foreground font-bold shadow-btn ring-4 ring-primary/15">
        {number}
      </div>
    </div>
  );
}

function LevelRow({
  level,
  isLast,
  onClaim,
}: {
  level: ProgressItem;
  isLast: boolean;
  onClaim?: (levelId: string, levelNumber: number, reward: number) => void;
}) {
  const pct = Math.min(
    100,
    Math.round((level.progress_value / level.requirement_value) * 100)
  );
  
  const progressLabel =
    level.level_type === "TEAM"
      ? `${level.progress_value} / ${level.requirement_value} members`
      : `${level.progress_value.toFixed(1)} / ${level.requirement_value} kg`;

  const requirementLabel =
    level.level_type === "TEAM"
      ? `Recruit ${level.requirement_value} Members`
      : `Collect ${level.requirement_value} kg Verified Waste`;

  return (
    <div className="relative flex gap-4">
      <div className="flex flex-col items-center">
        <LevelCircle status={level.status} number={level.level_number} />
        {!isLast && (
          <div
            className={`w-0.5 flex-1 my-1 ${
              level.status === "COMPLETED" || level.status === "CLAIMED"
                ? "bg-success"
                : "bg-border"
            }`}
            style={{ minHeight: 40 }}
          />
        )}
      </div>

      <div className="flex-1 pb-6">
        <div className="rounded-2xl border border-border bg-card p-4 shadow-card">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                {level.level_type === "TEAM" ? (
                  <Users className="h-3.5 w-3.5 text-primary" />
                ) : (
                  <User className="h-3.5 w-3.5 text-success" />
                )}
                {level.level_type === "TEAM" ? "Team" : "Personal"} Level {level.level_number}
              </div>
              <h3 className="mt-1 text-base font-bold text-foreground">{requirementLabel}</h3>
              <p className="mt-0.5 text-sm text-success font-semibold">{fmtINR(level.reward_amount)} reward</p>
            </div>
            <div className="flex flex-col items-end gap-2">
              {level.status === "LOCKED" && (
                <span className="inline-flex items-center gap-1 rounded-full bg-muted px-3 py-1 text-xs font-semibold text-muted-foreground">
                  <Lock className="h-3 w-3" /> Locked
                </span>
              )}
              {level.status === "IN_PROGRESS" && (
                <span className="rounded-full bg-primary-soft px-3 py-1 text-xs font-semibold text-primary border border-primary/10">
                  In Progress
                </span>
              )}
              {level.status === "COMPLETED" && (
                <button
                  onClick={() =>
                    onClaim &&
                    onClaim(level.id, level.level_number, level.reward_amount)
                  }
                  className="rounded-xl bg-success px-3 py-1.5 text-xs font-bold text-success-foreground shadow-sm hover:opacity-90 transition"
                >
                  Claim Reward →
                </button>
              )}
              {level.status === "CLAIMED" && (
                <span className="inline-flex items-center gap-1 rounded-full bg-success px-3 py-1 text-xs font-bold text-success-foreground">
                  <Check className="h-3 w-3" /> Reward Claimed
                </span>
              )}
            </div>
          </div>

          {level.status === "IN_PROGRESS" && (
            <div className="mt-3">
              <div className="flex items-center justify-between text-xs font-medium text-muted-foreground mb-1">
                <span>{progressLabel}</span>
                <span className="font-bold text-primary">{pct}%</span>
              </div>
              <div className="h-2 rounded-full bg-muted overflow-hidden">
                <div
                  className="h-full bg-primary transition-all duration-500"
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export function LevelTree({
  levels,
  onClaim,
}: {
  levels: ProgressItem[];
  onClaim?: (levelId: string, levelNumber: number, reward: number) => void;
}) {
  const team = levels.filter((l) => l.level_type === "TEAM");
  const personal = levels.filter((l) => l.level_type === "PERSONAL");

  return (
    <div className="space-y-4">
      {team.length > 0 && (
        <div>
          <div className="mb-6 rounded-2xl bg-nav-gradient p-4 text-white shadow-card">
            <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider opacity-90">
              <Users className="h-4 w-4" /> Team Challenges — Build Your Local Team
            </div>
            <p className="mt-1 text-sm opacity-90">
              Levels 1–6 unlock sequentially as your team grows in size together.
            </p>
          </div>
          {team.map((l, i) => (
            <LevelRow
              key={l.id}
              level={l}
              isLast={i === team.length - 1}
              onClaim={onClaim}
            />
          ))}
        </div>
      )}

      {personal.length > 0 && (
        <div className="pt-4">
          <div className="mb-6 rounded-2xl bg-success p-4 text-success-foreground shadow-card">
            <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider opacity-95">
              <Sparkles className="h-4 w-4" /> Personal Achievement Journey
            </div>
            <p className="mt-1 text-sm opacity-95">
              Levels 7–11 reward your individual waste recycling and collection actions.
            </p>
          </div>
          {personal.map((l, i) => (
            <LevelRow
              key={l.id}
              level={l}
              isLast={i === personal.length - 1}
              onClaim={onClaim}
            />
          ))}
        </div>
      )}
    </div>
  );
}
