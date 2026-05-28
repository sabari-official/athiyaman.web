import React, { useState } from 'react';
import { PublicLayout } from './Layout';
import { Mail, Phone, MapPin, Clock, Send, ShieldCheck } from 'lucide-react';
import { toast } from 'sonner';

export function PublicContact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: ''
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    toast.success("Message submitted successfully! Our Digital India team will respond shortly.");
    setFormData({
      name: '',
      email: '',
      phone: '',
      subject: '',
      message: ''
    });
    setTimeout(() => setSubmitted(false), 3000);
  };

  return (
    <PublicLayout>
      <div className="max-w-6xl mx-auto px-6 py-20 animate-fade-in-up">
        {/* Header Section */}
        <div className="text-center max-w-2xl mx-auto mb-16">
          <span className="px-3 py-1 rounded-full bg-primary/10 text-primary text-[10px] font-black uppercase tracking-wider">
            🇮🇳 Digital India Desk
          </span>
          <h1 className="text-4xl font-extrabold text-slate-800 tracking-tight mt-4">
            Connect With Athiyaman
          </h1>
          <p className="text-slate-500 text-sm mt-3 leading-relaxed">
            Have questions about waste collection, team operations, payouts, or technical verification? Drop us a line. We are here to assist you 24/7.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
          {/* Contact Details Column */}
          <div className="lg:col-span-5 space-y-6">
            <div className="bg-white/80 border border-slate-200 p-6 rounded-3xl shadow-sm hover:shadow-md transition">
              <h2 className="text-lg font-black text-slate-800 flex items-center gap-2 mb-6 border-b pb-3">
                <MapPin className="h-5 w-5 text-primary" /> Contact Details
              </h2>
              
              <div className="space-y-6 text-sm">
                <div className="flex gap-4">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary">
                    <MapPin className="h-5 w-5" />
                  </div>
                  <div>
                    <h4 className="font-extrabold text-slate-800">Headquarters</h4>
                    <p className="text-slate-500 mt-1 leading-relaxed">
                      Athiyaman Platform, Swachh Bharat Cell,<br />
                      Madurai, Tamil Nadu, PIN 625001
                    </p>
                  </div>
                </div>

                <div className="flex gap-4">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary">
                    <Phone className="h-5 w-5" />
                  </div>
                  <div>
                    <h4 className="font-extrabold text-slate-800">Helpline</h4>
                    <p className="text-slate-500 mt-1 font-semibold font-mono">
                      +91 944-555-0199 (Toll-Free Support)
                    </p>
                  </div>
                </div>

                <div className="flex gap-4">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary">
                    <Mail className="h-5 w-5" />
                  </div>
                  <div>
                    <h4 className="font-extrabold text-slate-800">Email Queries</h4>
                    <p className="text-slate-500 mt-1">
                      <a href="mailto:info@athiyaman.in" className="text-primary hover:underline font-semibold font-mono">
                        info@athiyaman.in
                      </a>
                    </p>
                  </div>
                </div>

                <div className="flex gap-4">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary">
                    <Clock className="h-5 w-5" />
                  </div>
                  <div>
                    <h4 className="font-extrabold text-slate-800">Office Timings</h4>
                    <p className="text-slate-500 mt-1 leading-relaxed">
                      Monday - Friday: 9:00 AM - 6:00 PM<br />
                      Saturday: 10:00 AM - 4:00 PM (Closed Sundays)
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-emerald-50/50 border border-emerald-200/60 p-6 rounded-3xl shadow-sm">
              <h3 className="text-sm font-extrabold text-emerald-800 flex items-center gap-1.5">
                <ShieldCheck className="h-4.5 w-4.5 text-emerald-600" /> Vetted Team Leaders Scheme
              </h3>
              <p className="text-xs text-emerald-700 mt-2 leading-relaxed">
                For partnerships, collection center permissions, or regional directives updates, please contact the central cell directly with your organization details at <a href="mailto:partnerships@athiyaman.in" className="underline font-bold font-mono">partnerships@athiyaman.in</a>.
              </p>
            </div>
          </div>

          {/* Contact Form Column */}
          <div className="lg:col-span-7">
            <div className="bg-white/80 border border-slate-200 p-8 rounded-[32px] shadow-xl relative overflow-hidden gov-tricolor-bar">
              <h2 className="text-xl font-black text-slate-800 tracking-tight mb-2">Send Secure Message</h2>
              <p className="text-xs text-slate-500 mb-6">Enter your details and inquiry category below</p>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid sm:grid-cols-2 gap-4">
                  <label className="block">
                    <span className="text-xs font-bold text-slate-700">Your Name *</span>
                    <input
                      type="text"
                      required
                      value={formData.name}
                      onChange={(e) => setFormData({...formData, name: e.target.value})}
                      className="input-field mt-1.5 h-11"
                      placeholder="e.g. Anand Kumar"
                    />
                  </label>

                  <label className="block">
                    <span className="text-xs font-bold text-slate-700">Email Address *</span>
                    <input
                      type="email"
                      required
                      value={formData.email}
                      onChange={(e) => setFormData({...formData, email: e.target.value})}
                      className="input-field mt-1.5 h-11"
                      placeholder="e.g. anand@example.com"
                    />
                  </label>
                </div>

                <div className="grid sm:grid-cols-2 gap-4">
                  <label className="block">
                    <span className="text-xs font-bold text-slate-700">Phone Number</span>
                    <input
                      type="text"
                      value={formData.phone}
                      onChange={(e) => setFormData({...formData, phone: e.target.value.replace(/\D/g, "")})}
                      className="input-field mt-1.5 h-11"
                      placeholder="10 digit mobile"
                    />
                  </label>

                  <label className="block">
                    <span className="text-xs font-bold text-slate-700">Subject Category *</span>
                    <input
                      type="text"
                      required
                      value={formData.subject}
                      onChange={(e) => setFormData({...formData, subject: e.target.value})}
                      className="input-field mt-1.5 h-11"
                      placeholder="e.g. Payout Request Status"
                    />
                  </label>
                </div>

                <label className="block">
                  <span className="text-xs font-bold text-slate-700">Detailed Message *</span>
                  <textarea
                    required
                    rows={4}
                    value={formData.message}
                    onChange={(e) => setFormData({...formData, message: e.target.value})}
                    className="input-field mt-1.5 py-3 resize-none"
                    placeholder="Describe your query in detail..."
                  />
                </label>

                <button
                  type="submit"
                  className="w-full h-11 rounded-2xl bg-primary text-white font-extrabold flex items-center justify-center gap-2 hover:opacity-95 shadow-btn transition duration-300 uppercase text-xs tracking-wider"
                >
                  <Send className="h-4 w-4" /> Send Message
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </PublicLayout>
  );
}
