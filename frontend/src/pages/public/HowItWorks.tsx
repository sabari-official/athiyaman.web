import React from 'react';
import { useNavigate } from 'react-router-dom';
import { PublicLayout } from './Layout';
import { Card, Button } from '../../components/athi';
import { Leaf, UserCheck, Shield, Award, MapPin, BadgePercent, ArrowRight } from 'lucide-react';

export function PublicHowItWorks() {
  const navigate = useNavigate();

  return (
    <PublicLayout>
      <div className="max-w-5xl mx-auto px-6 py-28 relative overflow-hidden animate-fade-in-up">
        {/* Floating Glowing Lights */}
        <div className="absolute top-[-10%] right-[-5%] w-[450px] h-[450px] rounded-full bg-emerald-500/5 blur-[95px] animate-pulse-glow pointer-events-none" />
        <div className="absolute bottom-[20%] left-[-10%] w-[400px] h-[400px] rounded-full bg-blue-500/5 blur-[85px] animate-pulse-glow pointer-events-none" style={{ animationDelay: '-3s' }} />

        {/* Unique Headings Layout */}
        <div className="text-center max-w-3xl mx-auto mb-20 space-y-6">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-2xl bg-white/60 backdrop-blur-md border border-white/50 text-primary text-xs font-black uppercase tracking-widest shadow-sm">
            ⚙️ Step-by-Step Walkthrough
          </div>
          <h1 className="text-4xl md:text-6xl font-black text-slate-900 tracking-tight leading-[1.1]">
            How the <span className="text-gradient">Athiyaman</span> Platform Works
          </h1>
          <p className="text-slate-600 text-lg font-medium leading-relaxed">
            Athiyaman bridges environmental responsibility and civic incentives using transparent technology, 
            local leadership, and immediate verification systems. Here is exactly how to participate.
          </p>
        </div>

        {/* Premium Translucent Invitation Box */}
        <div className="glass-card rounded-[32px] p-10 border border-white/70 shadow-2xl text-center mb-20 relative overflow-hidden transform hover:scale-[1.01] transition-all duration-300">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-emerald-500/5 pointer-events-none" />
          <h2 className="text-3xl font-black text-slate-800 tracking-tight leading-none">Ready to start making an impact?</h2>
          <p className="mt-4 text-slate-600 text-sm max-w-xl mx-auto leading-relaxed font-semibold">
            Fill out our simplified member registration form below. Once your leader reviews and approves, 
            you'll get your invite code to sign up!
          </p>
          <div className="mt-8 flex justify-center gap-4">
            <Button
              variant="primary"
              onClick={() => navigate('/join-member')}
              className="btn-primary"
            >
              Join as Member <ArrowRight className="h-4.5 w-4.5" />
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-14">
          {/* Section 1: Member Flow */}
          <div className="glass-card p-10 rounded-[32px] relative overflow-hidden hover:shadow-2xl hover:border-white/80 transition-all duration-300">
            <div className="absolute top-0 left-0 h-full w-2.5 bg-gradient-to-b from-blue-500 to-indigo-600" />
            
            <div className="flex flex-col md:flex-row gap-10 items-start">
              <div className="p-5 rounded-2xl bg-blue-50 text-primary mb-4 md:mb-0 shadow-sm border border-blue-100/50">
                <UserCheck className="h-10 w-12" />
              </div>
              <div className="flex-1 space-y-4">
                <h2 className="text-2xl font-black text-slate-800 tracking-tight flex items-center gap-3">
                  <span>1. How to Join as a Member</span>
                  <span className="text-[10px] font-black uppercase px-3.5 py-1.5 bg-blue-50 text-primary border border-blue-100 rounded-full">Citizen Track</span>
                </h2>
                
                <ol className="text-slate-600 space-y-4 ml-2 list-decimal pl-4 leading-relaxed text-sm font-medium">
                  <li>
                    <strong className="text-slate-800">Submit Application:</strong> Click the <strong>"Join as Member"</strong> button to fill out your name, contact info, physical address, and Aadhaar number.
                  </li>
                  <li>
                    <strong className="text-slate-800">Leader Verification:</strong> Local leaders in your PIN code review the pending list and approve registrations for their local roster.
                  </li>
                  <li>
                    <strong className="text-slate-800">Receive Invitation Link:</strong> Upon approval, your registration invite is sent directly to your phone via SMS/WhatsApp.
                  </li>
                  <li>
                    <strong className="text-slate-800">Complete Signup:</strong> Use your phone number and the approved referral code to create your account credentials and log in instantly.
                  </li>
                </ol>
                
                <div className="bg-blue-50/60 p-5 rounded-2xl text-xs text-primary font-bold leading-relaxed border border-blue-100/60 flex items-start gap-3">
                  <span className="text-base">💡</span>
                  <span><strong>Closed-Loop Safety:</strong> Restricting signups ensures every citizen profile maps to a valid local physical address, guaranteeing the community remains free of bots or fake records.</span>
                </div>
              </div>
            </div>
          </div>

          {/* Section 2: Leader Flow */}
          <div className="glass-card p-10 rounded-[32px] relative overflow-hidden hover:shadow-2xl hover:border-white/80 transition-all duration-300">
            <div className="absolute top-0 left-0 h-full w-2.5 bg-gradient-to-b from-emerald-500 to-success" />
            
            <div className="flex flex-col md:flex-row gap-10 items-start">
              <div className="p-5 rounded-2xl bg-emerald-50 text-success mb-4 md:mb-0 shadow-sm border border-emerald-100/50">
                <Shield className="h-10 w-12" />
              </div>
              <div className="flex-1 space-y-4">
                <h2 className="text-2xl font-black text-slate-800 tracking-tight flex items-center gap-3">
                  <span>2. How to Become a Team Leader</span>
                  <span className="text-[10px] font-black uppercase px-3.5 py-1.5 bg-emerald-50 text-success border border-emerald-100 rounded-full">Leader Track</span>
                </h2>
                
                <ol className="text-slate-600 space-y-4 ml-2 list-decimal pl-4 leading-relaxed text-sm font-medium">
                  <li>
                    <strong className="text-slate-800">Admin Dispatch Link:</strong> The registration page `/apply-leader` is unlisted. Admins generate unique application invite links and send them to vetted community leaders.
                  </li>
                  <li>
                    <strong className="text-slate-800">Fill Secure Form:</strong> Leaders submit their contact details, physical address, and Aadhaar card info.
                  </li>
                  <li>
                    <strong className="text-slate-800">Aadhaar & Pin Code Verification:</strong> System automatically validates the Aadhaar checksum and links to their postal zip code.
                  </li>
                  <li>
                    <strong className="text-slate-800">Generate Referral Codes:</strong> Once approved by the main administrator, Leaders can generate custom team referral codes to recruit members.
                  </li>
                </ol>
              </div>
            </div>
          </div>

          {/* Section 3: Earning System */}
          <div className="glass-card p-10 rounded-[32px] relative overflow-hidden hover:shadow-2xl hover:border-white/80 transition-all duration-300">
            <div className="absolute top-0 left-0 h-full w-2.5 bg-gradient-to-b from-indigo-500 to-purple-600" />
            
            <div className="flex flex-col md:flex-row gap-10 items-start">
              <div className="p-5 rounded-2xl bg-indigo-50 text-indigo-600 mb-4 md:mb-0 shadow-sm border border-indigo-100/50">
                <Award className="h-10 w-12" />
              </div>
              <div className="flex-1 space-y-4">
                <h2 className="text-2xl font-black text-slate-800 tracking-tight flex items-center gap-3">
                  <span>3. How to Submit & Earn Rewards</span>
                  <span className="text-[10px] font-black uppercase px-3.5 py-1.5 bg-indigo-50 text-indigo-600 border border-indigo-100 rounded-full">Reward Rails</span>
                </h2>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 my-6">
                  <div className="bg-white/60 backdrop-blur-md border border-white/50 p-6 rounded-2xl shadow-sm hover:scale-[1.02] transform transition-all">
                    <h3 className="font-extrabold text-slate-800 mb-3 flex items-center gap-2">
                      <MapPin className="h-5 w-5 text-blue-500" /> 1. Drop Off
                    </h3>
                    <p className="text-xs text-slate-500 leading-relaxed font-semibold">
                      Bring recyclable sorting waste to verified local collection centers listed in your dashboard map.
                    </p>
                  </div>
                  <div className="bg-white/60 backdrop-blur-md border border-white/50 p-6 rounded-2xl shadow-sm hover:scale-[1.02] transform transition-all">
                    <h3 className="font-extrabold text-slate-800 mb-3 flex items-center gap-2">
                      <UserCheck className="h-5 w-5 text-emerald-500" /> 2. Weighed & Logged
                    </h3>
                    <p className="text-xs text-slate-500 leading-relaxed font-semibold">
                      Center staff weigh the waste and log it directly in the app. Updates apply immediately to your profile!
                    </p>
                  </div>
                  <div className="bg-white/60 backdrop-blur-md border border-white/50 p-6 rounded-2xl shadow-sm hover:scale-[1.02] transform transition-all">
                    <h3 className="font-extrabold text-slate-800 mb-3 flex items-center gap-2">
                      <BadgePercent className="h-5 w-5 text-amber-500" /> 3. Payout Claimed
                    </h3>
                    <p className="text-xs text-slate-500 leading-relaxed font-semibold">
                      Milestone completions trigger claims which admins approve and disburse directly through verified bank rails.
                    </p>
                  </div>
                </div>
                
                <div className="bg-yellow-50/70 p-5 rounded-2xl border border-yellow-100 text-xs text-warning-foreground leading-relaxed font-bold flex items-start gap-3">
                  <span className="text-base">⚠️</span>
                  <span><strong>Locked Dashboard Access:</strong> Details on specific payments, milestone weights, and payout records are fully secured. You must sign in using your invite-only profile credentials to view them inside the dashboard panels.</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </PublicLayout>
  );
}
