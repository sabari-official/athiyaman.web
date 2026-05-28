import type { ReactNode } from "react";

type Variant = "PENDING" | "APPROVED" | "REJECTED" | "PAID" | "LOCKED" | "IN_PROGRESS" | "COMPLETED" | "CLAIMED" | "NOT_APPLICABLE";

const styles: Record<Variant, string> = {
  PENDING: "bg-warning-soft text-warning-foreground border border-warning/15",
  APPROVED: "bg-success-soft text-success border border-success/15",
  REJECTED: "bg-danger-soft text-danger border border-danger/15",
  PAID: "bg-success-soft text-success border border-success/15",
  LOCKED: "bg-muted text-muted-foreground border border-border",
  IN_PROGRESS: "bg-primary-soft text-primary border border-primary/10",
  COMPLETED: "bg-success-soft text-success border border-success/15",
  CLAIMED: "bg-success text-success-foreground",
  NOT_APPLICABLE: "bg-muted text-muted-foreground",
};

const labels: Record<Variant, string> = {
  PENDING: "Pending",
  APPROVED: "Approved",
  REJECTED: "Rejected",
  PAID: "Paid",
  LOCKED: "Locked",
  IN_PROGRESS: "In Progress",
  COMPLETED: "Completed",
  CLAIMED: "Claimed",
  NOT_APPLICABLE: "—",
};

export function StatusBadge({ status, icon }: { status: Variant; icon?: ReactNode }) {
  return (
    <span className={`inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-semibold ${styles[status]}`}>
      {icon}
      {labels[status]}
    </span>
  );
}
