import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../../components/athi';

export function PublicLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-tr from-slate-50 via-blue-50/30 to-emerald-50/20 relative">
      {/* Decorative Floating Glowing Lights */}
      <div className="absolute top-20 left-10 w-96 h-96 rounded-full bg-blue-300/10 blur-[80px] animate-pulse-glow pointer-events-none" />
      <div className="absolute top-1/2 right-10 w-[450px] h-[450px] rounded-full bg-emerald-300/5 blur-[100px] animate-pulse-glow pointer-events-none" style={{ animationDelay: '-4s' }} />

      {/* Navigation */}
      <nav className="bg-white/70 backdrop-blur-md border-b border-white/40 sticky top-0 z-40 transition-all duration-300 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-10">
              <h1 className="text-2xl font-black tracking-tight text-gradient transform hover:scale-[1.02] transition duration-200">
                <Link to="/" className="flex items-center gap-2">
                  <span>♻️</span>
                  <span>Athiyaman</span>
                </Link>
              </h1>
              <div className="hidden md:flex gap-8 text-sm font-semibold text-slate-600">
                <Link to="/about" className="hover:text-primary hover:translate-y-[-1px] transition-all duration-200">About</Link>
                <Link to="/how-it-works" className="hover:text-primary hover:translate-y-[-1px] transition-all duration-200">How it Works</Link>
                <Link to="/plans" className="hover:text-primary hover:translate-y-[-1px] transition-all duration-200">Plans & Info</Link>
                <Link to="/gallery" className="hover:text-primary hover:translate-y-[-1px] transition-all duration-200">Gallery</Link>
                <Link to="/contact" className="hover:text-primary hover:translate-y-[-1px] transition-all duration-200">Contact</Link>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <Link to="/login">
                <Button variant="primary" className="text-xs font-bold uppercase tracking-wider px-6 py-2">
                  Sign In
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-grow">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="font-bold mb-4">About Athiyaman</h3>
              <p className="text-gray-400 text-sm">Building a sustainable future through community-driven action and civic engagement.</p>
            </div>
            <div>
              <h3 className="font-bold mb-4">Quick Links</h3>
              <ul className="text-gray-400 text-sm space-y-2">
                <li><Link to="/about" className="hover:text-white">About Us</Link></li>
                <li><Link to="/how-it-works" className="hover:text-white">How It Works</Link></li>
                <li><Link to="/plans" className="hover:text-white">Plans</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold mb-4">Support</h3>
              <ul className="text-gray-400 text-sm space-y-2">
                <li><Link to="/contact" className="hover:text-white">Contact Us</Link></li>
                <li><a href="#" className="hover:text-white">FAQ</a></li>
                <li><a href="#" className="hover:text-white">Privacy Policy</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold mb-4">Contact</h3>
              <p className="text-gray-400 text-sm">
                Email: info@athiyaman.in<br />
                Phone: +91-XXXX-XXXX-XX
              </p>
            </div>
          </div>
          <div className="border-t border-gray-700 pt-6 text-center text-gray-400">
            <p>&copy; 2026 Athiyaman Platform. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
