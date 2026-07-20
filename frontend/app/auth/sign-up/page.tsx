'use client';

import { SignUpForm } from '@/components/auth/SignUpForm';
import Link from 'next/link';
import { useState } from 'react';

export default function SignUpPage() {
  const [isLoading, setIsLoading] = useState(false);

  const handleSignUp = async (name: string, email: string, password: string) => {
    setIsLoading(true);
    try {
      // This is a frontend-only implementation for demo purposes
      // In a real app, this would call your backend API
      console.log('[v0] Sign up attempt:', { name, email });

      // Simulate API call delay
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // For demo, just show success (in real app, validate and create account)
      console.log('[v0] Account created successfully');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Top Brand */}
      <div className="p-4 sm:p-6">
        <Link href="/" className="flex items-center gap-2 w-fit">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-gold to-amber">
            <span className="text-lg font-bold text-background">I</span>
          </div>
          <span className="font-bold text-text-primary hidden sm:inline">Intellex</span>
        </Link>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-md">
          {/* Background gradient effect */}
          <div className="absolute inset-0 -top-40 -z-10 opacity-20">
            <div className="absolute h-96 w-96 rounded-full bg-gold blur-3xl right-0"></div>
          </div>

          <SignUpForm onSubmit={handleSignUp} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
}
