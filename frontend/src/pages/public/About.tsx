import React from 'react';
import { PublicLayout } from './Layout';
import { Card } from '../../components/athi';

export function PublicAbout() {
  return (
    <PublicLayout>
      <div className="max-w-4xl mx-auto px-4 py-20">
        <h1 className="text-4xl font-bold mb-8">About Athiyaman</h1>

        <Card className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Our Mission</h2>
          <p className="text-gray-600 mb-4">
            Athiyaman is a community-driven platform designed to empower citizens to contribute to 
            environmental sustainability while building a stronger local economy. We believe that civic 
            participation should be transparent, rewarding, and inclusive.
          </p>
        </Card>

        <Card className="mb-8">
          <h2 className="text-2xl font-bold mb-4">What We Do</h2>
          <p className="text-gray-600 mb-4">
            We provide a digital ecosystem where:
          </p>
          <ul className="text-gray-600 space-y-2 ml-4 list-disc">
            <li>Citizens can collect and submit waste materials</li>
            <li>Community leaders can build and manage teams</li>
            <li>Everyone can track their progress through clear levels</li>
            <li>Contributions are directly rewarded with financial incentives</li>
            <li>All activities are transparent and auditable</li>
          </ul>
        </Card>

        <Card className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Our Vision</h2>
          <p className="text-gray-600">
            To create a leading civic engagement platform in India where individual micro-actions 
            translate directly into verifiable community growth, certified credentials, and financial rewards. 
            We aim to redefine civic responsibility by making it gamified, financially viable, and completely transparent.
          </p>
        </Card>

        <Card>
          <h2 className="text-2xl font-bold mb-4">Our Values</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <h3 className="font-bold mb-2">✓ Transparency</h3>
              <p className="text-gray-600 text-sm">Complete visibility into all processes and rewards.</p>
            </div>
            <div>
              <h3 className="font-bold mb-2">✓ Integrity</h3>
              <p className="text-gray-600 text-sm">Zero-compromise on data security and verification.</p>
            </div>
            <div>
              <h3 className="font-bold mb-2">✓ Inclusion</h3>
              <p className="text-gray-600 text-sm">Accessible to all citizens regardless of background.</p>
            </div>
            <div>
              <h3 className="font-bold mb-2">✓ Impact</h3>
              <p className="text-gray-600 text-sm">Real, measurable environmental and social change.</p>
            </div>
          </div>
        </Card>
      </div>
    </PublicLayout>
  );
}
