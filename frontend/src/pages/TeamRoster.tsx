import React from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";
import { fmtDate } from "../lib/format";
import { Users, User, ClipboardList, Award, Recycle } from "lucide-react";
import { StatCard } from "../components/athi/StatCard";

interface MemberOut {
  id: string;
  full_name: string;
  email: string;
  is_active: boolean;
  joined_at: string | null;
  total_waste_kg: number;
  approved_waste_kg: number;
  pending_waste_kg: number;
  waste_submissions: number;
}

interface TeamDetailOut {
  id: string;
  name: string;
  leader_name: string;
  total_members: number;
  active_members: number;
  members: MemberOut[];
}

export function TeamRoster() {
  const { data: team, isLoading } = useQuery({
    queryKey: ["leader-team"],
    queryFn: async () => {
      const { data } = await api.get("/api/v1/leader/team");
      return data as TeamDetailOut;
    },
  });

  const members = team?.members || [];
  const totalApproved = members.reduce((sum, m) => sum + m.approved_waste_kg, 0);
  const totalSubmissions = members.reduce((sum, m) => sum + m.waste_submissions, 0);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-extrabold text-foreground tracking-tight flex items-center gap-2">
          <Users className="h-7 w-7 text-primary" /> Team Leader Roster
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Monitor your local citizen group progress, submissions counts, and approved waste weights.
        </p>
      </div>

      {/* Metrics Row */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Team Name"
          value={team?.name || "Loading…"}
          sub={`Leader: ${team?.leader_name || "—"}`}
          icon={<Award className="h-5 w-5" />}
          tone="primary"
        />

        <StatCard
          label="Total Recruits"
          value={`${team?.total_members || 0} Citizens`}
          sub={`${team?.active_members || 0} active members`}
          icon={<Users className="h-5 w-5" />}
          tone="success"
        />

        <StatCard
          label="Team Recycled Waste"
          value={`${totalApproved.toFixed(1)} KG`}
          sub="Combined verified weight"
          icon={<Recycle className="h-5 w-5" />}
          tone="success"
        />

        <StatCard
          label="Total Logged Entries"
          value={`${totalSubmissions} Deposits`}
          sub="Combined waste entries"
          icon={<ClipboardList className="h-5 w-5" />}
          tone="warning"
        />
      </div>

      {/* Roster Table Card */}
      <div className="card">
        <h2 className="text-base font-bold text-foreground mb-4 flex items-center gap-1.5">
          <ClipboardList className="h-4.5 w-4.5 text-primary" /> Active Citizens Roster
        </h2>

        {isLoading ? (
          <div className="flex h-48 items-center justify-center text-muted-foreground text-xs font-semibold">
            Loading team rosters…
          </div>
        ) : members.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-48 text-center bg-slate-50 border border-dashed border-border p-6 rounded-2xl">
            <span className="text-2xl">👥</span>
            <p className="mt-2 text-sm font-semibold text-foreground">No Citizens Recruited Yet</p>
            <p className="mt-1 text-xs text-muted-foreground max-w-xs">
              Generate a **TEAM** invitation code in the referrals section and share it with citizens to build your group.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto rounded-xl border border-border bg-white">
            <table className="min-w-full divide-y divide-border text-left">
              <thead className="bg-muted text-[10px] font-bold text-muted-foreground uppercase tracking-widest">
                <tr>
                  <th className="px-4 py-3.5">Member Name</th>
                  <th className="px-4 py-3.5">Email Address</th>
                  <th className="px-4 py-3.5">Enrollment Date</th>
                  <th className="px-4 py-3.5">Deposits Logs</th>
                  <th className="px-4 py-3.5">Approved Weights</th>
                  <th className="px-4 py-3.5">Account Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border text-xs text-foreground">
                {members.map((member) => (
                  <tr key={member.id} className="hover:bg-slate-50 transition">
                    <td className="px-4 py-4 flex items-center gap-2 font-bold text-foreground">
                      <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary-soft text-primary text-[10px] font-extrabold uppercase">
                        {member.full_name[0]}
                      </div>
                      {member.full_name}
                    </td>
                    <td className="px-4 py-4 text-muted-foreground">{member.email}</td>
                    <td className="px-4 py-4 text-muted-foreground">{fmtDate(member.joined_at || "")}</td>
                    <td className="px-4 py-4 text-muted-foreground font-semibold">
                      {member.waste_submissions} deposits
                    </td>
                    <td className="px-4 py-4 text-success font-bold">
                      {member.approved_waste_kg.toFixed(1)} KG
                    </td>
                    <td className="px-4 py-4">
                      <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-[10px] font-extrabold uppercase tracking-wide ${member.is_active ? "bg-success-soft text-success" : "bg-muted text-muted-foreground"}`}>
                        {member.is_active ? "Active" : "Inactive"}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
export default TeamRoster;
