import React from 'react';
import { PublicLayout } from './Layout';
import { Card } from '../../components/athi';

export function PublicGallery() {
  return (
    <PublicLayout>
      <div className="max-w-6xl mx-auto px-4 py-20">
        <h1 className="text-4xl font-bold mb-8 text-center">Community Gallery</h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="bg-gray-300 rounded-lg h-64 flex items-center justify-center">
              <div className="text-center text-white">
                <div className="text-6xl mb-2">📸</div>
                <p>Community Image {i}</p>
              </div>
            </div>
          ))}
        </div>

        <Card className="bg-blue-50 border-2 border-blue-200">
          <h2 className="text-2xl font-bold mb-4">📸 Gallery Coming Soon</h2>
          <p className="text-gray-600 mb-4">
            We're building a comprehensive gallery showcasing our community members, collection centers, 
            and the positive impact of waste management initiatives across the country.
          </p>
          <p className="text-gray-600">
            Check back soon to see photos from:
          </p>
          <ul className="text-gray-600 space-y-2 ml-4 list-disc mt-2">
            <li>Community waste collection events</li>
            <li>Collection center operations</li>
            <li>Team building activities</li>
            <li>Environmental impact projects</li>
          </ul>
        </Card>
      </div>
    </PublicLayout>
  );
}
