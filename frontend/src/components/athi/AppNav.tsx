import { Link, useNavigate, useLocation } from "react-router-dom";
import { Leaf, LogOut, Menu, X, Bell } from "lucide-react";
import { useState } from "react";
import { useAuth } from "../../lib/auth";
import { initials } from "../../lib/format";

export interface NavLink {
  to: string;
  label: string;
  badge?: number;
}

export function AppNav({ links }: { links: NavLink[] }) {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [open, setOpen] = useState(false);
  const pathname = location.pathname;

  const handleSignOut = () => {
    signOut();
    navigate("/login", { replace: true });
  };

  return (
    <header className="sticky top-0 z-40 bg-nav-gradient text-white shadow-card">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3.5 sm:px-6">
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-2.5 font-bold text-lg hover:opacity-95 transition">
          <div className="flex h-9.5 w-9.5 items-center justify-center rounded-xl bg-white/15 backdrop-blur shadow-sm">
            <Leaf className="h-5 w-5 text-white" />
          </div>
          <div>
            <p className="font-extrabold leading-none text-sm tracking-tight">Athiyaman</p>
            <p className="text-[9px] uppercase tracking-widest opacity-80 mt-0.5">Digital India</p>
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <nav className="hidden lg:flex items-center gap-1.5">
          {links.map((l) => {
            const active =
              pathname === l.to ||
              (l.to !== "/dashboard" && pathname.startsWith(l.to));
            return (
              <Link
                key={l.to}
                to={l.to}
                className={`relative rounded-xl px-3.5 py-2 text-xs font-semibold tracking-wide uppercase transition-all duration-150 ${
                  active ? "bg-white/20 shadow-sm" : "hover:bg-white/10"
                }`}
              >
                {l.label}
                {l.badge ? (
                  <span className="absolute -right-1.5 -top-1.5 flex h-4.5 min-w-4.5 items-center justify-center rounded-full bg-danger px-1 text-[9px] font-bold text-white shadow-sm animate-pulse">
                    {l.badge}
                  </span>
                ) : null}
              </Link>
            );
          })}
        </nav>

        {/* Desktop Profile & Logout Actions */}
        <div className="hidden lg:flex items-center gap-4.5">
          {user && (
            <div className="flex items-center gap-2.5">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white/15 backdrop-blur border border-white/10 text-xs font-bold shadow-sm">
                {initials(user.username)}
              </div>
              <div className="text-left leading-tight">
                <p className="text-xs font-bold tracking-tight">{user.username}</p>
                <span className="inline-block px-1.5 py-0.5 mt-0.5 rounded bg-success-soft text-success text-[8px] font-extrabold uppercase tracking-widest">
                  {user.role}
                </span>
              </div>
            </div>
          )}
          <button
            onClick={handleSignOut}
            className="inline-flex items-center gap-1.5 rounded-xl bg-white/15 px-3.5 py-2 text-xs font-bold tracking-wide uppercase hover:bg-white/25 border border-white/5 transition-all shadow-sm"
          >
            <LogOut className="h-3.5 w-3.5" /> Sign Out
          </button>
        </div>

        {/* Mobile menu toggle */}
        <button
          className="lg:hidden rounded-xl bg-white/15 p-2 shadow-sm border border-white/5"
          onClick={() => setOpen((o) => !o)}
          aria-label="Toggle Menu Navigation"
        >
          {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {/* Mobile Menu Drawer */}
      {open && (
        <div className="lg:hidden border-t border-white/10 bg-deep-blue px-4 py-4 space-y-1 shadow-card animate-fadeIn">
          {links.map((l) => (
            <Link
              key={l.to}
              to={l.to}
              onClick={() => setOpen(false)}
              className="flex items-center justify-between rounded-xl px-3 py-3 text-xs font-bold uppercase tracking-wide hover:bg-white/10 transition"
            >
              <span>{l.label}</span>
              {l.badge ? (
                <span className="rounded-full bg-danger px-2.5 py-0.5 text-[9px] font-bold shadow-sm">
                  {l.badge}
                </span>
              ) : null}
            </Link>
          ))}
          
          {user && (
            <div className="mt-4 pt-4 border-t border-white/10 flex items-center justify-between rounded-xl bg-white/5 p-3">
              <div className="flex items-center gap-2.5">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white/15 text-xs font-bold">
                  {initials(user.username)}
                </div>
                <div>
                  <p className="text-xs font-bold tracking-tight">{user.username}</p>
                  <span className="inline-block px-1.5 py-0.5 rounded bg-success-soft text-success text-[8px] font-extrabold uppercase tracking-widest mt-0.5">
                    {user.role}
                  </span>
                </div>
              </div>
              <button
                onClick={handleSignOut}
                className="rounded-xl bg-white/20 px-3.5 py-2 text-xs font-bold tracking-wide uppercase hover:bg-white/25 transition shadow-sm border border-white/5"
              >
                Sign Out
              </button>
            </div>
          )}
        </div>
      )}
    </header>
  );
}
