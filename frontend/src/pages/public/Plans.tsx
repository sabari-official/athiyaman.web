import React from 'react';
import { PublicLayout } from './Layout';
import { Card, Badge } from '../../components/athi';

export function PublicPlans() {
  return (
    <PublicLayout>
      <div className="max-w-4xl mx-auto px-4 py-20">
        <h1 className="text-4xl font-bold mb-8">Plans & Information</h1>

        <Card className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Phase 1: Digital India (Current)</h2>
          <p className="text-gray-600 mb-4">
            The foundation of Athiyaman, focused on building the digital infrastructure for:
          </p>
          <ul className="text-gray-600 space-y-2 ml-4 list-disc">
            <li>Waste collection and verification</li>
            <li>Team formation and management</li>
            <li>User level progression (personal and team-based)</li>
            <li>Reward claiming and payment processing</li>
            <li>Digital record transparency and auditability</li>
          </ul>
        </Card>

        <Card className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Phase 2: Skill India (Coming Soon)</h2>
          <p className="text-gray-600 mb-4">
            Introducing skills training and employment opportunities:
          </p>
          <ul className="text-gray-600 space-y-2 ml-4 list-disc">
            <li>Technical skill training modules</li>
            <li>Course certifications</li>
            <li>Job placement assistance</li>
            <li>Salary tracking and management</li>
          </ul>
          <Badge variant="warning" className="mt-4">Coming in Phase 2</Badge>
        </Card>

        <Card className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Phase 3: Clean India (Future)</h2>
          <p className="text-gray-600 mb-4">
            Scaling waste processing and logistics:
          </p>
          <ul className="text-gray-600 space-y-2 ml-4 list-disc">
            <li>Advanced waste processing facilities</li>
            <li>Logistics and transportation management</li>
            <li>District-level coordination</li>
            <li>Environmental reporting and analytics</li>
          </ul>
          <Badge variant="danger" className="mt-4">Coming in Phase 3</Badge>
        </Card>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 my-12">
          <Card>
            <h3 className="text-xl font-bold mb-4">💰 Payment & Rewards</h3>
            <p className="text-gray-600 text-sm mb-4">
              Earnings are calculated based on verified waste contributions and team growth milestones.
            </p>
            <div className="text-sm text-gray-600">
              ✓ Transparent calculation<br/>
              ✓ Direct bank transfers<br/>
              ✓ No hidden charges<br/>
              <strong className="text-blue-600">Complete details in Instructions</strong>
            </div>
          </Card>

          <Card>
            <h3 className="text-xl font-bold mb-4">🎓 Training & Growth</h3>
            <p className="text-gray-600 text-sm mb-4">
              Skill India Phase 2 will introduce certifications and career development.
            </p>
            <div className="text-sm text-gray-600">
              ✓ Online courses<br/>
              ✓ Certifications<br/>
              ✓ Job placement<br/>
              <strong className="text-yellow-600">Coming Soon</strong>
            </div>
          </Card>
        </div>

        <Card>
          <h2 className="text-2xl font-bold mb-4">💡 General Information</h2>
          <div className="space-y-4 text-gray-600">
            <div>
              <p><strong>🔒 Data Security:</strong> All your personal information is encrypted and protected by industry-leading security standards.</p>
            </div>
            <div>
              <p><strong>📋 Transparency:</strong> Track every waste submission, level progression, and reward in real-time through your dashboard.</p>
            </div>
            <div>
              <p><strong>👥 Community:</strong> Join thousands of citizens already making a difference in their communities.</p>
            </div>
            <div>
              <p><strong>🌍 Impact:</strong> Every submission contributes to environmental sustainability and community development.</p>
            </div>
          </div>
          <div className="bg-blue-50 p-4 rounded mt-6 text-sm">
            <strong>Note:</strong> For specific information about payment structures, level requirements, and detailed benefits, 
            please log in to access the <strong>Instructions</strong> page.
          </div>
        </Card>
      </div>
    </PublicLayout>
  );
}
