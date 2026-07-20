'use client';

import { Navbar } from '@/components/layout/Navbar';
import { Sidebar } from '@/components/layout/Sidebar';
import { useState } from 'react';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // Mock conversations data
  const conversations = [
    {
      id: '1',
      title: 'AI Best Practices',
      lastMessageAt: new Date(Date.now() - 3600000),
    },
    {
      id: '2',
      title: 'React Performance Tips',
      lastMessageAt: new Date(Date.now() - 7200000),
    },
    {
      id: '3',
      title: 'API Design Discussion',
      lastMessageAt: new Date(Date.now() - 86400000),
    },
  ];

  return (
    <div className="h-screen flex flex-col bg-background">
      <Navbar
        onMenuToggle={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        isMenuOpen={isMobileMenuOpen}
      />

      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <Sidebar
          isOpen={!isMobileMenuOpen}
          conversations={conversations}
          currentConversationId="1"
          onNewConversation={() => console.log('[v0] New conversation')}
        />

        {/* Mobile Sidebar Overlay */}
        {isMobileMenuOpen && (
          <div
            className="fixed inset-0 bg-background/80 backdrop-blur-sm md:hidden z-30"
            onClick={() => setIsMobileMenuOpen(false)}
          />
        )}

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
