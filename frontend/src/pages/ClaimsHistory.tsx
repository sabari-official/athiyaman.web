import React, { useState } from "react";
import { useMyClaims } from "../lib/hooks";
import { StatusBadge } from "../components/athi/StatusBadge";
import { fmtDate, fmtINR } from "../lib/format";
import { Landmark, Award, ClipboardList } from "lucide-react";

export function ClaimsHistory() {
  const [page, setPage] = useState(1);
  const { data, isLoading } = useMyClaims(page, 10);
  const items = data?.items || [];
  const total = data?.total || 0;
  const totalPages = Math.ceil(total / 10);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-foreground tracking-tight flex items-center gap-2">
          <Landmark className="h-6 w-6 text-warning" /> Reward Milestone Claims
        </h1>
        <p className="mt-1 text-xs text-muted-foreground">
          Track details of cash payouts claimed upon complete milestones progression.
        </p>
      </div>

      {/* Roster Card */}
      <div className="card">
        <h2 className="text-base font-bold text-foreground mb-4 flex items-center gap-1.5">
          <ClipboardList className="h-4.5 w-4.5 text-primary" /> Submitted Claims Roster
        </h2>

        {isLoading ? (
          <div className="flex h-48 items-center justify-center text-muted-foreground text-xs font-semibold">
            Loading reward claims…
          </div>
        ) : items.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-48 text-center bg-muted/30 rounded-2xl border border-dashed border-border p-6">
            <span className="text-2xl text-muted-foreground">🏆</span>
            <p className="mt-2 text-sm font-semibold text-foreground">No Payout Claims Found</p>
            <p className="mt-1 text-xs text-muted-foreground max-w-xs">
              Complete level milestones in your main dashboard to qualify for cash reward claim requests.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="overflow-x-auto rounded-xl border border-border">
              <table className="min-w-full divide-y divide-border text-left">
                <thead className="bg-muted text-[10px] font-bold text-muted-foreground uppercase tracking-widest">
                  <tr>
                    <th className="px-4 py-3.5">Claim ID</th>
                    <th className="px-4 py-3.5">Milestone Type</th>
                    <th className="px-4 py-3.5">Target Level</th>
                    <th className="px-4 py-3.5">Payout Amount</th>
                    <th className="px-4 py-3.5">Claimed Date</th>
                    <th className="px-4 py-3.5">Payment Status</th>
                    <th className="px-4 py-3.5">Audit note</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border text-xs text-foreground bg-white">
                  {items.map((item) => (
                    <tr key={item.claim_id} className="hover:bg-slate-50 transition">
                      <td className="px-4 py-4 font-mono font-bold text-[10px] select-all text-muted-foreground">
                        {item.claim_id.slice(0, 8)}...
                      </td>
                      <td className="px-4 py-4 font-bold text-foreground">
                        {item.claim_type === "TEAM_REWARD" ? "👥 Team Milestones" : "👤 Personal Milestones"}
                      </td>
                      <td className="px-4 py-4 text-muted-foreground font-semibold">
                        Level {item.level_number}
                      </td>
                      <td className="px-4 py-4 font-bold text-success">
                        {fmtINR(item.amount)}
                      </td>
                      <td className="px-4 py-4 text-muted-foreground">
                        {fmtDate(item.requested_at)}
                      </td>
                      <td className="px-4 py-4">
                        <StatusBadge status={item.status} />
                      </td>
                      <td className="px-4 py-4 text-muted-foreground italic">
                        {item.rejection_reason || "—"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination Controls */}
            {totalPages > 1 && (
              <div className="flex items-center justify-between border-t border-border pt-4 text-xs">
                <p className="text-muted-foreground">
                  Showing page <span className="font-semibold text-foreground">{page}</span> of{" "}
                  <span className="font-semibold text-foreground">{totalPages}</span>
                </p>
                <div className="flex gap-2">
                  <button
                    disabled={page === 1}
                    onClick={() => setPage((p) => p - 1)}
                    className="h-9 px-3.5 rounded-xl border border-border bg-white font-bold hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
                  >
                    Previous
                  </button>
                  <button
                    disabled={page === totalPages}
                    onClick={() => setPage((p) => p + 1)}
                    className="h-9 px-3.5 rounded-xl border border-border bg-white font-bold hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
                  >
                    Next
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
export default ClaimsHistory;
