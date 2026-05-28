import React, { useState } from 'react';
import { PublicLayout } from './Layout';
import { Card, Button, Input, Alert } from '../../components/athi';

export function PublicContact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: ''
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: any) => {
    e.preventDefault();
    // Submit logic here
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 3000);
  };

  return (
    <PublicLayout>
      <div className="max-w-4xl mx-auto px-4 py-20">
        <h1 className="text-4xl font-bold mb-8">Contact Us</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Contact Form */}
          <Card>
            <h2 className="text-2xl font-bold mb-6">Send us a Message</h2>
            {submitted && <Alert type="success" message="Message sent successfully! We'll get back to you soon." />}
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                label="Name"
                placeholder="Your full name"
                value={formData.name}
                onChange={(e: any) => setFormData({...formData, name: e.target.value})}
                required
              />
              <Input
                label="Email"
                type="email"
                placeholder="your@email.com"
                value={formData.email}
                onChange={(e: any) => setFormData({...formData, email: e.target.value})}
                required
              />
              <Input
                label="Phone"
                placeholder="10-digit phone number"
                value={formData.phone}
                onChange={(e: any) => setFormData({...formData, phone: e.target.value})}
              />
              <Input
                label="Subject"
                placeholder="What is your inquiry about?"
                value={formData.subject}
                onChange={(e: any) => setFormData({...formData, subject: e.target.value})}
                required
              />
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Message</label>
                <textarea
                  placeholder="Your message here..."
                  rows={4}
                  value={formData.message}
                  onChange={(e: any) => setFormData({...formData, message: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <Button variant="primary" type="submit" className="w-full">
                Send Message
              </Button>
            </form>
          </Card>

          {/* Contact Information */}
          <div className="space-y-6">
            <Card>
              <h3 className="text-xl font-bold mb-4">📍 Address</h3>
              <p className="text-gray-600">
                Athiyaman Platform<br />
                Madurai, Tamil Nadu<br />
                India
              </p>
            </Card>

            <Card>
              <h3 className="text-xl font-bold mb-4">📞 Phone</h3>
              <p className="text-gray-600">
                <a href="tel:+91XXXXXXXXXX" className="text-blue-600 hover:underline">
                  +91-XXXX-XXXX-XX
                </a>
              </p>
            </Card>

            <Card>
              <h3 className="text-xl font-bold mb-4">📧 Email</h3>
              <p className="text-gray-600">
                <a href="mailto:info@athiyaman.in" className="text-blue-600 hover:underline">
                  info@athiyaman.in
                </a>
              </p>
            </Card>

            <Card>
              <h3 className="text-xl font-bold mb-4">🕐 Business Hours</h3>
              <p className="text-gray-600">
                Monday - Friday: 9:00 AM - 6:00 PM<br />
                Saturday: 10:00 AM - 4:00 PM<br />
                Sunday: Closed
              </p>
            </Card>

            <Card>
              <h3 className="text-xl font-bold mb-4">❓ Leader Application Support</h3>
              <p className="text-gray-600 text-sm mb-4">
                For questions about becoming a team leader, please contact us with:
              </p>
              <ul className="text-gray-600 text-sm space-y-1 ml-4 list-disc">
                <li>Your full name</li>
                <li>Phone number</li>
                <li>Expected team size</li>
                <li>District/Area details</li>
              </ul>
            </Card>
          </div>
        </div>

        <Card className="mt-8 bg-green-50 border-2 border-green-200">
          <h2 className="text-2xl font-bold mb-4">🤝 Partnership Opportunities</h2>
          <p className="text-gray-600 mb-4">
            Interested in partnering with Athiyaman for collection centers, waste processing, or community initiatives? 
            We'd love to hear from you!
          </p>
          <p className="text-gray-600">
            Reach out to our partnerships team at: <a href="mailto:partnerships@athiyaman.in" className="text-green-600 underline">
              partnerships@athiyaman.in
            </a>
          </p>
        </Card>
      </div>
    </PublicLayout>
  );
}
