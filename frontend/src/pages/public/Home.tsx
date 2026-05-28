import React from 'react';
import { useNavigate } from 'react-router-dom';
import { PublicLayout } from './Layout';
import { Button, Card } from '../../components/athi';
import { Leaf, ArrowRight, ShieldCheck, Award, Zap, Users, Recycle, Globe } from 'lucide-react';

export function PublicHome() {
  const navigate = useNavigate();

  return (
    <PublicLayout>
      {/* Hero Section - Asymmetric Premium Layout */}
      <section className="max-w-7xl mx-auto px-6 py-28 relative overflow-hidden animate-fade-in-up">
        {/* Intricate Floating Glowing Orbs */}
        <div className="absolute top-[-15%] left-[-15%] w-[600px] h-[600px] rounded-full bg-blue-500/10 blur-[110px] animate-pulse-glow pointer-events-none" />
        <div className="absolute bottom-[5%] right-[-10%] w-[550px] h-[550px] rounded-full bg-emerald-500/5 blur-[120px] animate-pulse-glow pointer-events-none animate-float" style={{ animationDuration: '10s' }} />

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-16 items-center relative z-10">
          {/* Asymmetric Offset Text Block */}
          <div className="lg:col-span-7 space-y-8 text-left lg:pr-6">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-2xl bg-white/60 backdrop-blur-md border border-white/50 text-primary text-xs font-black uppercase tracking-widest shadow-sm">
              <Leaf className="h-4.5 w-4.5 text-success animate-bounce" /> Onboarding India's Green Future
            </div>
            
            <h1 className="text-5xl md:text-7xl font-black text-slate-900 tracking-tight leading-[1.05] drop-shadow-sm">
              Turn Civic Action <br />
              Into <span className="text-gradient">Real Rewards</span>
            </h1>
            
            <p className="text-lg md:text-xl text-slate-600 leading-relaxed max-w-2xl font-medium">
              Join thousands of verified citizens making a direct environmental difference. 
              Collect recyclables, build local clean-up teams, track progress, and claim milestone payouts securely.
            </p>
            
            <div className="flex flex-wrap gap-4 pt-4">
              <Button 
                variant="primary" 
                onClick={() => navigate('/how-it-works')}
                className="btn-primary flex items-center gap-2"
              >
                Join as Member <ArrowRight className="h-5 w-5" />
              </Button>
              <Button
                variant="outline"
                onClick={() => navigate('/how-it-works')}
                className="btn-outline"
              >
                Learn How It Works
              </Button>
            </div>
          </div>
          
          {/* Asymmetric Offset Visual Block */}
          <div className="lg:col-span-5 relative lg:mt-[-20px] transform hover:rotate-1 transition-all duration-500">
            {/* Visual Glass Box with Offset Borders */}
            <div className="absolute inset-0 bg-gradient-to-tr from-blue-500/10 to-emerald-500/10 rounded-[36px] blur-3xl transform rotate-6 scale-95" />
            <div className="glass-card rounded-[36px] p-10 shadow-2xl relative border border-white/70 animate-float">
              <div className="absolute top-6 right-6 text-[10px] font-extrabold uppercase tracking-widest px-3.5 py-1.5 bg-emerald-50/80 text-success border border-emerald-100/50 rounded-full backdrop-blur-sm shadow-sm">
                Integrity Shield
              </div>
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-tr from-primary to-secondary text-white shadow-lg mb-8">
                <Leaf className="h-8 w-8 animate-spin" style={{ animationDuration: '10s' }} />
              </div>
              <h3 className="text-2xl font-black text-slate-800 tracking-tight leading-none">Athiyaman Civic Loop</h3>
              <p className="mt-4 text-slate-600 leading-relaxed text-sm font-medium">
                A highly secure, audited, closed-loop civic engagement network designed for Digital India. Fully transparent and 100% verified.
              </p>
              
              <div className="mt-8 space-y-4 pt-8 border-t border-slate-200/60">
                <div className="flex items-center gap-3 text-xs font-extrabold text-slate-500">
                  <span className="h-2.5 w-2.5 rounded-full bg-success animate-ping" />
                  <span>Aadhaar Integrations Active</span>
                </div>
                <div className="flex items-center gap-3 text-xs font-extrabold text-slate-500">
                  <span className="h-2.5 w-2.5 rounded-full bg-blue-500" />
                  <span>Dynamic Level Milestone Payouts</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Banner - Cleaned from "10+" Reference */}
      <section className="bg-slate-900 text-white py-16 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-950/40 to-emerald-950/20 opacity-60" />
        <div className="max-w-7xl mx-auto px-6 relative z-10 grid grid-cols-2 md:grid-cols-4 gap-10 text-center">
          <div>
            <h4 className="text-3xl md:text-5xl font-black text-gradient">24/7</h4>
            <p className="text-slate-400 text-xs md:text-sm font-bold uppercase tracking-widest mt-2">Immutable Auditing</p>
          </div>
          <div>
            <h4 className="text-3xl md:text-5xl font-black text-gradient">Multiple</h4>
            <p className="text-slate-400 text-xs md:text-sm font-bold uppercase tracking-widest mt-2">Level Milestones</p>
          </div>
          <div>
            <h4 className="text-3xl md:text-5xl font-black text-gradient">100%</h4>
            <p className="text-slate-400 text-xs md:text-sm font-bold uppercase tracking-widest mt-2">Aadhaar Verification</p>
          </div>
          <div>
            <h4 className="text-3xl md:text-5xl font-black text-gradient">Instant</h4>
            <p className="text-slate-400 text-xs md:text-sm font-bold uppercase tracking-widest mt-2">Milestone Releases</p>
          </div>
        </div>
      </section>

      {/* Asymmetric Stepped Features Loop */}
      <section className="py-28 max-w-7xl mx-auto px-6 relative">
        <div className="text-center max-w-3xl mx-auto mb-20 space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 text-success text-[10px] font-black uppercase tracking-widest border border-emerald-100/50">
            Platform Workflow
          </div>
          <h2 className="text-4xl md:text-5xl font-black text-slate-900 tracking-tight leading-none">Structured Civic Loop</h2>
          <p className="text-slate-600 font-medium text-lg">A clean, transparent, four-step cycle that turns environmental care into real rewards.</p>
        </div>
        
        {/* Diagonal Asymmetric Step Layout */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <Card className="card hover:scale-[1.03] transition duration-300 relative group overflow-hidden md:translate-y-[-10px]">
            <div className="absolute top-0 left-0 w-2.5 h-full bg-blue-500 transform scale-y-0 group-hover:scale-y-100 transition-all duration-300" />
            <div className="text-5xl mb-6">📱</div>
            <h3 className="font-extrabold text-xl mb-3 text-slate-800 tracking-tight">1. Apply</h3>
            <p className="text-slate-600 text-sm leading-relaxed font-medium">Submit a secure application to get registered under a designated leader.</p>
          </Card>
          <Card className="card hover:scale-[1.03] transition duration-300 relative group overflow-hidden md:translate-y-[10px]">
            <div className="absolute top-0 left-0 w-2.5 h-full bg-emerald-500 transform scale-y-0 group-hover:scale-y-100 transition-all duration-300" />
            <div className="text-5xl mb-6">📍</div>
            <h3 className="font-extrabold text-xl mb-3 text-slate-800 tracking-tight">2. Submit</h3>
            <p className="text-slate-600 text-sm leading-relaxed font-medium">Deposit sorted waste materials at authorized local collection centers.</p>
          </Card>
          <Card className="card hover:scale-[1.03] transition duration-300 relative group overflow-hidden md:translate-y-[-10px]">
            <div className="absolute top-0 left-0 w-2.5 h-full bg-indigo-500 transform scale-y-0 group-hover:scale-y-100 transition-all duration-300" />
            <div className="text-5xl mb-6">📈</div>
            <h3 className="font-extrabold text-xl mb-3 text-slate-800 tracking-tight">3. Level Up</h3>
            <p className="text-slate-600 text-sm leading-relaxed font-medium">Automated SQL triggers securely compile progression updates as targets are hit.</p>
          </Card>
          <Card className="card hover:scale-[1.03] transition duration-300 relative group overflow-hidden md:translate-y-[10px]">
            <div className="absolute top-0 left-0 w-2.5 h-full bg-amber-500 transform scale-y-0 group-hover:scale-y-100 transition-all duration-300" />
            <div className="text-5xl mb-6">💰</div>
            <h3 className="font-extrabold text-xl mb-3 text-slate-800 tracking-tight">4. Claim</h3>
            <p className="text-slate-600 text-sm leading-relaxed font-medium">Review level payout metrics and request verified ledger transfers instantly.</p>
          </Card>
        </div>
      </section>

      {/* Unique Design Info Cards Grid */}
      <section className="py-28 bg-white/30 backdrop-blur-sm border-t border-slate-200/40 relative">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center max-w-3xl mx-auto mb-20 space-y-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 text-primary text-[10px] font-black uppercase tracking-widest border border-blue-100/50">
              Platform Values
            </div>
            <h2 className="text-4xl md:text-5xl font-black text-slate-900 tracking-tight leading-none">Built on Absolute Integrity</h2>
            <p className="text-slate-600 font-medium text-lg">Designed to maintain the highest standard for citizens, leaders, and managers.</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
            <div className="glass-card p-10 rounded-[32px] relative overflow-hidden group hover:scale-[1.03] hover:shadow-xl transition duration-300">
              <div className="h-14 w-14 rounded-2xl bg-blue-50 flex items-center justify-center text-primary mb-8 shadow-sm">
                <ShieldCheck className="h-7 w-7" />
              </div>
              <h3 className="text-2xl font-extrabold mb-4 text-slate-800 tracking-tight">Vetted Profiles</h3>
              <p className="text-slate-600 text-sm leading-relaxed font-medium">
                All citizen records, contact metrics, and Aadhaar numbers are fully cross-referenced to eliminate synthetic profiles and duplicates.
              </p>
            </div>
            
            <div className="glass-card p-10 rounded-[32px] relative overflow-hidden group hover:scale-[1.03] hover:shadow-xl transition duration-300">
              <div className="h-14 w-14 rounded-2xl bg-emerald-50 flex items-center justify-center text-success mb-8 shadow-sm">
                <Users className="h-7 w-7" />
              </div>
              <h3 className="text-2xl font-extrabold mb-4 text-slate-800 tracking-tight">Decentralized Rosters</h3>
              <p className="text-slate-600 text-sm leading-relaxed font-medium">
                Leaders build and manage local teams in closed-loops based on postal pincodes, ensuring localized accountability.
              </p>
            </div>
            
            <div className="glass-card p-10 rounded-[32px] relative overflow-hidden group hover:scale-[1.03] hover:shadow-xl transition duration-300">
              <div className="h-14 w-14 rounded-2xl bg-amber-50 flex items-center justify-center text-warning mb-8 shadow-sm">
                <Award className="h-7 w-7" />
              </div>
              <h3 className="text-2xl font-extrabold mb-4 text-slate-800 tracking-tight">Guaranteed Payouts</h3>
              <p className="text-slate-600 text-sm leading-relaxed font-medium">
                Each completed milestone triggers automated reward claims that are verified and paid out directly through secure bank rails.
              </p>
            </div>
          </div>
        </div>
      </section>
    </PublicLayout>
  );
}
