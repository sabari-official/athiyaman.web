import type { ReactNode } from "react";

type Tone = "primary" | "success" | "warning" | "neutral";
const toneBg: Record<Tone, string> = {
  primary: "bg-primary-soft text-primary border border-primary/10 shadow-sm",
  success: "bg-success-soft text-success border border-success/10 shadow-sm",
  warning: "bg-warning-soft text-warning-foreground border border-warning/10 shadow-sm",
  neutral: "bg-slate-50 text-slate-500 border border-slate-100 shadow-sm",
};

export function StatCard({
  label,
  value,
  sub,
  icon,
  tone = "primary",
}: {
  label: string;
  value: ReactNode;
  sub?: ReactNode;
  icon?: ReactNode;
  tone?: Tone;
}) {
  return (
    <div className="rounded-2xl bg-white/70 backdrop-blur-md border border-white/40 p-6 shadow-card hover:shadow-lg hover:scale-[1.02] transform transition-all duration-300 relative overflow-hidden group">
      {/* Dynamic Hover Glow Spot */}
      <div className="absolute -right-6 -bottom-6 w-20 h-20 rounded-full bg-primary/5 blur-xl group-hover:bg-primary/10 transition-all duration-300 pointer-events-none" />
      
      <div className="flex items-start justify-between gap-3 relative z-10">
        <div>
          <p className="text-[10px] font-extrabold uppercase tracking-widest text-slate-400">{label}</p>
          <p className="mt-2 text-2xl md:text-3xl font-black text-slate-800 tracking-tight leading-none">{value}</p>
          {sub && <p className="mt-2 text-xs text-slate-500 font-medium leading-relaxed">{sub}</p>}
        </div>
        {icon && (
          <div className={`flex h-12 w-12 items-center justify-center rounded-2xl transition-transform duration-300 group-hover:scale-110 ${toneBg[tone]}`}>
            {icon}
          </div>
        )}
      </div>
    </div>
  );
}
