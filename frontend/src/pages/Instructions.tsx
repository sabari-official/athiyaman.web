import React, { useState } from 'react';
import { useAuth } from '../lib/auth';
import { Card, Badge, Table } from '../components/athi';

export function Instructions() {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('overview');

  const tabs = ['overview', 'levels', 'payments', 'waste', 'teams', 'claims', 'support'];

  const renderContent = () => {
    switch(activeTab) {
      case 'overview':
        return <OverviewTab />;
      case 'levels':
        return <LevelsTab />;
      case 'payments':
        return <PaymentsTab />;
      case 'waste':
        return <WasteTab />;
      case 'teams':
        return <TeamsTab />;
      case 'claims':
        return <ClaimsTab />;
      case 'support':
        return <SupportTab />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 py-10 animate-fade-in-up">
      <div className="max-w-6xl mx-auto px-6">
        <div className="mb-10 text-center md:text-left">
          <span className="px-3 py-1 rounded-full bg-primary/10 text-primary text-[10px] font-black uppercase tracking-wider">
            🇮🇳 Government Guidelines
          </span>
          <h1 className="text-4xl font-black text-slate-800 tracking-tight mt-3">
            Athiyaman Portal Instructions
          </h1>
          <p className="text-slate-500 text-sm mt-1">Complete official guide to utilizing the portal, rules verification, and level progressions.</p>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-8 overflow-x-auto pb-2 scrollbar-thin">
          {tabs.map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-5 py-2.5 rounded-2xl font-extrabold capitalize whitespace-nowrap transition-all duration-300 text-xs tracking-wider border select-none ${
                activeTab === tab
                  ? 'bg-primary border-primary text-white shadow-md'
                  : 'bg-white/80 border-slate-200 text-slate-600 hover:bg-white hover:text-slate-800'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="space-y-6">
          {renderContent()}
        </div>
      </div>
    </div>
  );
}

function OverviewTab() {
  return (
    <>
      <Card>
        <h2 className="text-2xl font-bold mb-4">Welcome to Athiyaman</h2>
        <p className="text-gray-600 mb-4">
          Athiyaman is a comprehensive civic engagement platform that rewards you for contributing to 
          environmental sustainability. This guide provides complete information about how to maximize your 
          earnings and impact.
        </p>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">Quick Start Guide</h2>
        <ol className="text-gray-600 space-y-3 ml-4 list-decimal">
          <li><strong>Complete Your Profile:</strong> Fill in your personal information and Aadhaar verification</li>
          <li><strong>Accept Platform Rules:</strong> Review and accept the terms and conditions</li>
          <li><strong>Update Payment Details:</strong> Add your bank account for reward transfers</li>
          <li><strong>Find Collection Centers:</strong> Locate nearby waste submission points</li>
          <li><strong>Start Submitting Waste:</strong> Begin earning rewards immediately</li>
          <li><strong>Build Your Team (Optional):</strong> Invite others as a team leader for additional benefits</li>
        </ol>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">Platform Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-blue-50 p-4 rounded">
            <h3 className="font-bold mb-2">📱 Dashboard</h3>
            <p className="text-sm text-gray-600">Real-time overview of your progress, earnings, and team status.</p>
          </div>
          <div className="bg-green-50 p-4 rounded">
            <h3 className="font-bold mb-2">📦 Waste Submission</h3>
            <p className="text-sm text-gray-600">Submit waste at collection centers and track verification status.</p>
          </div>
          <div className="bg-purple-50 p-4 rounded">
            <h3 className="font-bold mb-2">📈 Level Progress</h3>
            <p className="text-sm text-gray-600">Monitor your progression through 11 levels with increasing rewards.</p>
          </div>
          <div className="bg-yellow-50 p-4 rounded">
            <h3 className="font-bold mb-2">💰 Reward Claims</h3>
            <p className="text-sm text-gray-600">View and claim your earned rewards with transparent calculations.</p>
          </div>
          <div className="bg-pink-50 p-4 rounded">
            <h3 className="font-bold mb-2">👥 Team Management</h3>
            <p className="text-sm text-gray-600">Build and manage your team, earn team-based rewards.</p>
          </div>
          <div className="bg-orange-50 p-4 rounded">
            <h3 className="font-bold mb-2">📊 Analytics</h3>
            <p className="text-sm text-gray-600">Detailed reports of your contributions and earnings.</p>
          </div>
        </div>
      </Card>
    </>
  );
}

function LevelsTab() {
  const levels = [
    { num: 1, name: 'Bronze', req: '50 kg waste', reward: '₹500', personal: true },
    { num: 2, name: 'Silver', req: '150 kg waste', reward: '₹1,500', personal: true },
    { num: 3, name: 'Gold', req: '300 kg waste', reward: '₹3,000', personal: true },
    { num: 4, name: 'Platinum', req: '500 kg waste', reward: '₹5,000', personal: true },
    { num: 5, name: 'Diamond', req: '750 kg waste', reward: '₹7,500', personal: true },
    { num: 6, name: 'Team Lead', req: '10 team members', reward: '₹5,000', team: true },
    { num: 7, name: 'Team Platinum', req: '25 team members', reward: '₹12,500', team: true },
    { num: 8, name: 'Elite', req: '50 team members', reward: '₹25,000', team: true },
    { num: 9, name: 'Master', req: '100 team members', reward: '₹50,000', team: true },
    { num: 10, name: 'Legend', req: '200 team members', reward: '₹100,000', team: true },
  ];

  return (
    <>
      <Card>
        <h2 className="text-2xl font-bold mb-4">Level System Overview</h2>
        <p className="text-gray-600 mb-4">
          Athiyaman uses a 10-level progression system designed to reward consistent contribution:
        </p>
        <ul className="text-gray-600 space-y-2 ml-4 list-disc">
          <li><strong>Levels 1-5: Personal Levels</strong> - Based on your individual waste contributions</li>
          <li><strong>Levels 6-10: Team Levels</strong> - Based on your team's growth and achievements (team leaders only)</li>
          <li><strong>Cumulative Progression:</strong> Requirements build on each other</li>
          <li><strong>Rewards Unlock:</strong> Each level achievement unlocks new benefits</li>
        </ul>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">Level Requirements & Rewards</h2>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead className="bg-gray-100">
              <tr>
                <th className="border border-gray-300 p-3 text-left">Level</th>
                <th className="border border-gray-300 p-3 text-left">Name</th>
                <th className="border border-gray-300 p-3 text-left">Requirement</th>
                <th className="border border-gray-300 p-3 text-left">Reward</th>
                <th className="border border-gray-300 p-3 text-left">Type</th>
              </tr>
            </thead>
            <tbody>
              {levels.map((lvl, idx) => (
                <tr key={idx} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  <td className="border border-gray-300 p-3 font-bold">{lvl.num}</td>
                  <td className="border border-gray-300 p-3">{lvl.name}</td>
                  <td className="border border-gray-300 p-3">{lvl.req}</td>
                  <td className="border border-gray-300 p-3 font-bold text-green-600">{lvl.reward}</td>
                  <td className="border border-gray-300 p-3">
                    {lvl.personal && <Badge variant="default">Personal</Badge>}
                    {lvl.team && <Badge variant="success">Team</Badge>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">How Levels Work</h2>
        <div className="space-y-4">
          <div>
            <h3 className="font-bold mb-2">📈 Progress Tracking</h3>
            <p className="text-gray-600">
              Your progress is automatically calculated based on verified waste submissions. Check your dashboard 
              to see current progress toward the next level.
            </p>
          </div>
          <div>
            <h3 className="font-bold mb-2">🎯 Automatic Updates</h3>
            <p className="text-gray-600">
              Levels are checked and updated daily. When you meet the requirements, the level is unlocked automatically.
            </p>
          </div>
          <div>
            <h3 className="font-bold mb-2">💡 Tips for Faster Progression</h3>
            <ul className="text-gray-600 space-y-1 ml-4 list-disc">
              <li>Submit waste regularly at collection centers</li>
              <li>Ensure all submissions are properly verified</li>
              <li>For team leaders: Focus on recruiting quality team members</li>
              <li>Encourage team members to be active contributors</li>
            </ul>
          </div>
        </div>
      </Card>
    </>
  );
}

function PaymentsTab() {
  return (
    <>
      <Card>
        <h2 className="text-2xl font-bold mb-4">Payment Processing</h2>
        <p className="text-gray-600 mb-4">
          All rewards are processed through direct bank transfers to your registered account.
        </p>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">Payment Timeline</h2>
        <div className="space-y-4">
          <div className="bg-blue-50 p-4 rounded border-l-4 border-blue-600">
            <h3 className="font-bold mb-2">Step 1: Waste Submitted</h3>
            <p className="text-sm text-gray-600">You submit waste at a collection center</p>
            <p className="text-xs text-gray-500 mt-1">Immediately recorded in system</p>
          </div>
          <div className="bg-green-50 p-4 rounded border-l-4 border-green-600">
            <h3 className="font-bold mb-2">Step 2: Verification</h3>
            <p className="text-sm text-gray-600">Collection center staff verifies weight and quality</p>
            <p className="text-xs text-gray-500 mt-1">Same day or next day</p>
          </div>
          <div className="bg-purple-50 p-4 rounded border-l-4 border-purple-600">
            <h3 className="font-bold mb-2">Step 3: Points Credited</h3>
            <p className="text-sm text-gray-600">Points added to your level progression</p>
            <p className="text-xs text-gray-500 mt-1">Within 24 hours of verification</p>
          </div>
          <div className="bg-yellow-50 p-4 rounded border-l-4 border-yellow-600">
            <h3 className="font-bold mb-2">Step 4: Level Achievement</h3>
            <p className="text-sm text-gray-600">When you reach level requirements, rewards unlock</p>
            <p className="text-xs text-gray-500 mt-1">Checked daily</p>
          </div>
          <div className="bg-orange-50 p-4 rounded border-l-4 border-orange-600">
            <h3 className="font-bold mb-2">Step 5: Claim Reward</h3>
            <p className="text-sm text-gray-600">Submit claim request through dashboard</p>
            <p className="text-xs text-gray-500 mt-1">Available immediately after level achievement</p>
          </div>
          <div className="bg-pink-50 p-4 rounded border-l-4 border-pink-600">
            <h3 className="font-bold mb-2">Step 6: Admin Approval</h3>
            <p className="text-sm text-gray-600">Admin reviews and approves your claim</p>
            <p className="text-xs text-gray-500 mt-1">Usually 2-3 business days</p>
          </div>
          <div className="bg-red-50 p-4 rounded border-l-4 border-red-600">
            <h3 className="font-bold mb-2">Step 7: Payment Transfer</h3>
            <p className="text-sm text-gray-600">Funds transferred to your bank account</p>
            <p className="text-xs text-gray-500 mt-1">3-5 business days after approval</p>
          </div>
        </div>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">Bank Account Management</h2>
        <ul className="text-gray-600 space-y-2 ml-4 list-disc">
          <li>Update your bank details in your profile settings</li>
          <li>Ensure your account name matches your registered name</li>
          <li>All transfers are done via NEFT/RTGS for security</li>
          <li>Keep your bank account active and operational</li>
          <li>Notify us immediately if you change your account</li>
        </ul>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">Payment FAQs</h2>
        <div className="space-y-4">
          <div>
            <p className="font-bold text-gray-800">Q: How often are payments processed?</p>
            <p className="text-gray-600">A: Payments are processed weekly on Fridays for all approved claims from the week.</p>
          </div>
          <div>
            <p className="font-bold text-gray-800">Q: Is there a minimum payout amount?</p>
            <p className="text-gray-600">A: Minimum payout is ₹100. Claims below this amount are accumulated for the next week.</p>
          </div>
          <div>
            <p className="font-bold text-gray-800">Q: What if my payment fails?</p>
            <p className="text-gray-600">A: Failed payments are retried automatically. Contact support if issue persists.</p>
          </div>
          <div>
            <p className="font-bold text-gray-800">Q: Are there any deductions or taxes?</p>
            <p className="text-gray-600">A: Rewards are subject to applicable GST. No hidden charges are deducted.</p>
          </div>
        </div>
      </Card>
    </>
  );
}

function WasteTab() {
  return (
    <>
      <Card>
        <h2 className="text-2xl font-bold mb-4">Waste Submission Guide</h2>
        <p className="text-gray-600 mb-4">
          Waste submission is the core of the Athiyaman platform. Here's how to maximize your earnings.
        </p>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">Acceptable Waste Types</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-green-50 p-4 rounded">
            <h3 className="font-bold mb-2">✓ Accepted</h3>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Plastic bottles & containers</li>
              <li>• Metal cans & scraps</li>
              <li>• Paper & cardboard</li>
              <li>• Glass bottles</li>
              <li>• Aluminum foil & cans</li>
              <li>• Mixed dry waste</li>
            </ul>
          </div>
          <div className="bg-red-50 p-4 rounded">
            <h3 className="font-bold mb-2">✗ Not Accepted</h3>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Wet or organic waste</li>
              <li>• Hazardous materials</li>
              <li>• Electronic waste (without prior arrangement)</li>
              <li>• Medical waste</li>
              <li>• Contaminated items</li>
              <li>• Loose materials</li>
            </ul>
          </div>
        </div>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">Submission Process</h2>
        <ol className="text-gray-600 space-y-3 ml-4 list-decimal">
          <li><strong>Find Collection Center:</strong> Search for nearby centers using the map in your dashboard</li>
          <li><strong>Prepare Waste:</strong> Sort and clean your waste materials</li>
          <li><strong>Visit Center:</strong> Bring materials to the collection center during operating hours</li>
          <li><strong>Weighing:</strong> Staff will weigh your materials (minimum 0.1 kg, maximum 50 kg per submission)</li>
          <li><strong>Verification:</strong> Quality check is performed</li>
          <li><strong>Receipt:</strong> You receive a submission receipt with reference number</li>
          <li><strong>Record Update:</strong> Your dashboard is updated with the submission</li>
        </ol>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">Weight & Pricing</h2>
        <div className="bg-yellow-50 p-4 rounded mb-4 border-l-4 border-yellow-600">
          <p className="text-gray-800 font-bold mb-2">📋 Pricing Structure</p>
          <p className="text-sm text-gray-600 mb-2">Prices vary based on waste type and quality:</p>
          <ul className="text-sm text-gray-600 space-y-1 ml-4 list-disc">
            <li>Premium waste (clean, sorted): ₹5-15/kg</li>
            <li>Standard waste (reasonably sorted): ₹3-8/kg</li>
            <li>Mixed waste: ₹2-5/kg</li>
          </ul>
          <p className="text-xs text-gray-500 mt-2">Actual prices set by collection centers</p>
        </div>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">Tips for Successful Submissions</h2>
        <ul className="text-gray-600 space-y-2 ml-4 list-disc">
          <li>Clean waste is valued higher - wash bottles and remove labels if possible</li>
          <li>Sort waste by type for faster processing</li>
          <li>Submit regularly to maintain consistent level progression</li>
          <li>Keep your submission receipts for reference</li>
          <li>Peak hours: Early morning or late evening (less crowded)</li>
          <li>Build relationships with center staff for priority service</li>
        </ul>
      </Card>
    </>
  );
}

function TeamsTab() {
  return (
    <>
      <Card>
        <h2 className="text-2xl font-bold mb-4">Team Leadership Guide</h2>
        <p className="text-gray-600 mb-4">
          Team leaders unlock additional earning opportunities through team growth and performance.
        </p>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">Becoming a Team Leader</h2>
        <ol className="text-gray-600 space-y-3 ml-4 list-decimal">
          <li><strong>Apply:</strong> Submit a leadership application through "Apply as Leader" page</li>
          <li><strong>Verification:</strong> Admin team reviews your application (3-5 days)</li>
          <li><strong>Approval:</strong> Receive leadership approval notification</li>
          <li><strong>Team Creation:</strong> Create your team and set team details</li>
          <li><strong>Generate Codes:</strong> Create referral codes to invite members</li>
          <li><strong>Build Team:</strong> Invite members and manage their progress</li>
        </ol>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">Team Benefits</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-blue-50 p-4 rounded">
            <h3 className="font-bold mb-2">Leadership Rewards</h3>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>✓ Team level progression rewards</li>
              <li>✓ Up to ₹100,000 at Legend level</li>
              <li>✓ Team performance bonuses</li>
              <li>✓ Recognition and status</li>
            </ul>
          </div>
          <div className="bg-green-50 p-4 rounded">
            <h3 className="font-bold mb-2">Management Tools</h3>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>✓ Member roster management</li>
              <li>✓ Performance analytics</li>
              <li>✓ Team communication tools</li>
              <li>✓ Referral code generation</li>
            </ul>
          </div>
        </div>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">Team Requirements</h2>
        <div className="space-y-3">
          <div className="border-l-4 border-blue-600 pl-4">
            <p className="font-bold text-gray-800">Level 6: Team Lead</p>
            <p className="text-gray-600">10 active team members</p>
          </div>
          <div className="border-l-4 border-green-600 pl-4">
            <p className="font-bold text-gray-800">Level 7: Team Platinum</p>
            <p className="text-gray-600">25 active team members + ₹5,000 collective waste</p>
          </div>
          <div className="border-l-4 border-purple-600 pl-4">
            <p className="font-bold text-gray-800">Level 8: Elite</p>
            <p className="text-gray-600">50 active team members + ₹15,000 collective waste</p>
          </div>
          <div className="border-l-4 border-orange-600 pl-4">
            <p className="font-bold text-gray-800">Level 9: Master</p>
            <p className="text-gray-600">100 active team members + ₹35,000 collective waste</p>
          </div>
          <div className="border-l-4 border-red-600 pl-4">
            <p className="font-bold text-gray-800">Level 10: Legend</p>
            <p className="text-gray-600">200 active team members + ₹75,000 collective waste</p>
          </div>
        </div>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">Team Management Best Practices</h2>
        <ul className="text-gray-600 space-y-2 ml-4 list-disc">
          <li>Recruit members from your local area for better coordination</li>
          <li>Provide support and guidance to new members</li>
          <li>Organize regular waste collection drives</li>
          <li>Monitor member activity and provide incentives</li>
          <li>Maintain regular communication with your team</li>
          <li>Share success stories to motivate members</li>
        </ul>
      </Card>
    </>
  );
}

function ClaimsTab() {
  return (
    <>
      <Card>
        <h2 className="text-2xl font-bold mb-4">Reward Claims Guide</h2>
        <p className="text-gray-600 mb-4">
          Learn how to submit and track your reward claims for level achievements.
        </p>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">How to Submit a Claim</h2>
        <ol className="text-gray-600 space-y-3 ml-4 list-decimal">
          <li><strong>Check Achievement:</strong> Verify you've unlocked a new level (dashboard shows "Claim Available")</li>
          <li><strong>Go to Claims:</strong> Navigate to "Claims History" in your dashboard</li>
          <li><strong>Submit Claim:</strong> Click "Claim Reward" button for the level</li>
          <li><strong>Verify Details:</strong> Review claim details and confirm submission</li>
          <li><strong>Track Status:</strong> Monitor claim status (Pending → Approved → Processing → Paid)</li>
        </ol>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">Claim Status Explained</h2>
        <div className="space-y-3">
          <div className="bg-yellow-50 p-4 rounded border-l-4 border-yellow-600">
            <p className="font-bold text-yellow-800">⏳ Pending</p>
            <p className="text-sm text-gray-600">Claim submitted, waiting for admin review</p>
          </div>
          <div className="bg-green-50 p-4 rounded border-l-4 border-green-600">
            <p className="font-bold text-green-800">✅ Approved</p>
            <p className="text-sm text-gray-600">Claim verified and approved by admin</p>
          </div>
          <div className="bg-blue-50 p-4 rounded border-l-4 border-blue-600">
            <p className="font-bold text-blue-800">⚙️ Processing</p>
            <p className="text-sm text-gray-600">Payment being processed through bank</p>
          </div>
          <div className="bg-purple-50 p-4 rounded border-l-4 border-purple-600">
            <p className="font-bold text-purple-800">💰 Paid</p>
            <p className="text-sm text-gray-600">Payment successfully transferred to your account</p>
          </div>
        </div>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">Common Issues & Solutions</h2>
        <div className="space-y-4">
          <div>
            <p className="font-bold text-gray-800">Q: Can I submit multiple claims at once?</p>
            <p className="text-gray-600">A: Yes, you can claim multiple levels if you've achieved them.</p>
          </div>
          <div>
            <p className="font-bold text-gray-800">Q: What if my claim is rejected?</p>
            <p className="text-gray-600">A: You'll receive an explanation. Common reasons include incomplete profile or verification pending.</p>
          </div>
          <div>
            <p className="font-bold text-gray-800">Q: Can I cancel a claim?</p>
            <p className="text-gray-600">A: Yes, you can cancel claims in Pending or Approved status.</p>
          </div>
          <div>
            <p className="font-bold text-gray-800">Q: How long until payment arrives?</p>
            <p className="text-gray-600">A: Typically 3-5 business days after approval.</p>
          </div>
        </div>
      </Card>
    </>
  );
}

function SupportTab() {
  return (
    <>
      <Card>
        <h2 className="text-2xl font-bold mb-4">Support & Help</h2>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">Contact Support</h2>
        <div className="space-y-4">
          <div className="bg-blue-50 p-4 rounded">
            <p className="font-bold text-gray-800">📧 Email Support</p>
            <p className="text-gray-600">support@athiyaman.in</p>
            <p className="text-sm text-gray-500">Response time: 24-48 hours</p>
          </div>
          <div className="bg-green-50 p-4 rounded">
            <p className="font-bold text-gray-800">📞 Phone Support</p>
            <p className="text-gray-600">+91-XXXX-XXXX-XX</p>
            <p className="text-sm text-gray-500">Monday-Friday: 9 AM - 6 PM</p>
          </div>
          <div className="bg-purple-50 p-4 rounded">
            <p className="font-bold text-gray-800">💬 Live Chat</p>
            <p className="text-gray-600">Available in-app (coming soon)</p>
            <p className="text-sm text-gray-500">Real-time support from our team</p>
          </div>
        </div>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-4">Frequently Asked Questions</h2>
        <div className="space-y-4">
          <div>
            <p className="font-bold text-gray-800">Q: How do I update my profile?</p>
            <p className="text-gray-600">A: Go to Dashboard → Profile Settings. You can update most details anytime.</p>
          </div>
          <div>
            <p className="font-bold text-gray-800">Q: What if I forget my password?</p>
            <p className="text-gray-600">A: Click "Forgot Password" on login page and follow recovery instructions.</p>
          </div>
          <div>
            <p className="font-bold text-gray-800">Q: How do I change my phone number?</p>
            <p className="text-gray-600">A: Contact support with identity proof to verify the change request.</p>
          </div>
          <div>
            <p className="font-bold text-gray-800">Q: Can I delete my account?</p>
            <p className="text-gray-600">A: Contact support. Account deletion may affect pending claims and payouts.</p>
          </div>
        </div>
      </Card>

      <Card className="bg-green-50 border-2 border-green-200">
        <h2 className="text-2xl font-bold mb-4">🎯 Additional Resources</h2>
        <ul className="text-gray-600 space-y-2 ml-4 list-disc">
          <li><a href="#" className="text-green-600 underline">Platform Blog</a> - Latest updates and tips</li>
          <li><a href="#" className="text-green-600 underline">Video Tutorials</a> - Step-by-step guides</li>
          <li><a href="#" className="text-green-600 underline">Community Forum</a> - Connect with other members</li>
          <li><a href="#" className="text-green-600 underline">Safety & Security</a> - How we protect your data</li>
        </ul>
      </Card>
    </>
  );
}
