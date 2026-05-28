import React, { useState } from "react";
import { useNotifications, useMarkNotificationRead } from "../lib/hooks";
import { timeAgo } from "../lib/format";
import { Bell, Mail, MailOpen, ClipboardList } from "lucide-react";

export function NotificationsCenter() {
  const [page, setPage] = useState(1);
  const { data, isLoading } = useNotifications(page, 10);
  const markReadMutation = useMarkNotificationRead();

  const items = data?.items || [];
  const total = data?.total || 0;
  const totalPages = Math.ceil(total / 10);

  const getToneBorder = (type: string, read: boolean) => {
    if (read) return "border-border bg-white opacity-70";
    switch (type) {
      case "ALERT":
        return "border-danger/35 bg-danger-soft/10";
      case "WARNING":
        return "border-warning/35 bg-warning-soft/10";
      case "SUCCESS":
        return "border-success/35 bg-success-soft/10";
      default:
        return "border-primary/25 bg-primary-soft/10";
    }
  };

  const getToneIcon = (type: string) => {
    switch (type) {
      case "ALERT":
        return "text-danger bg-danger-soft";
      case "WARNING":
        return "text-warning bg-warning-soft";
      case "SUCCESS":
        return "text-success bg-success-soft";
      default:
        return "text-primary bg-primary-soft";
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-foreground tracking-tight flex items-center gap-2">
          <Bell className="h-6 w-6 text-primary" /> Bulletins & Announcements
        </h1>
        <p className="mt-1 text-xs text-muted-foreground">
          View broadcast notifications and alerts issued by platform administrators.
        </p>
      </div>

      {/* Notifications list */}
      <div className="card">
        <h2 className="text-base font-bold text-foreground mb-5 flex items-center gap-1.5">
          <ClipboardList className="h-4.5 w-4.5 text-primary" /> Delivery Inbox
        </h2>

        {isLoading ? (
          <div className="flex h-48 items-center justify-center text-muted-foreground text-xs font-semibold">
            Loading notifications…
          </div>
        ) : items.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-48 text-center bg-muted/30 rounded-2xl border border-dashed border-border p-6">
            <span className="text-2xl text-muted-foreground">📬</span>
            <p className="mt-2 text-sm font-semibold text-foreground">Inbox is Empty</p>
            <p className="mt-1 text-xs text-muted-foreground">
              You will receive push updates here when admins issue alerts or approve payout milestones.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="space-y-3">
              {items.map((log) => (
                <div
                  key={log.id}
                  className={`flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 rounded-2xl border transition-all ${getToneBorder(
                    log.notification.notification_type,
                    log.is_read
                  )}`}
                >
                  <div className="flex gap-3">
                    <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl font-bold text-xs ${getToneIcon(log.notification.notification_type)}`}>
                      {log.is_read ? <MailOpen className="h-4.5 w-4.5" /> : <Mail className="h-4.5 w-4.5" />}
                    </div>
                    <div>
                      <h4 className={`text-sm font-bold text-foreground flex items-center gap-2`}>
                        {log.notification.title}
                        {!log.is_read && (
                          <span className="h-2 w-2 rounded-full bg-danger inline-block animate-ping" />
                        )}
                      </h4>
                      <p className="mt-1 text-xs text-muted-foreground max-w-2xl leading-relaxed">
                        {log.notification.message}
                      </p>
                      <span className="mt-2 text-[10px] text-muted-foreground font-semibold block">
                        Delivered {timeAgo(log.delivered_at)}
                      </span>
                    </div>
                  </div>

                  {!log.is_read && (
                    <button
                      onClick={() => markReadMutation.mutate(log.id)}
                      className="shrink-0 h-9 px-4 rounded-xl border border-border bg-white text-xs font-bold text-foreground hover:bg-slate-50 transition shadow-sm"
                    >
                      Mark Read
                    </button>
                  )}
                </div>
              ))}
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
export default NotificationsCenter;
