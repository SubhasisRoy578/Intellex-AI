'use client';

import Link from 'next/link';
import { useState } from 'react';
import { motion } from 'framer-motion';
import { Mail, Loader2, CheckCircle2 } from 'lucide-react';

export default function VerifyEmailPage() {
  const [code, setCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isVerified, setIsVerified] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    setIsLoading(true);
    try {
      // Simulate verification
      await new Promise((resolve) => setTimeout(resolve, 1000));
      console.log('[v0] Email verification code submitted:', code);
      setIsVerified(true);
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
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="w-full max-w-md"
        >
          <div className="absolute inset-0 -top-40 -z-10 opacity-20">
            <div className="absolute h-96 w-96 rounded-full bg-gold blur-3xl right-0"></div>
          </div>

          {isVerified ? (
            <div className="text-center">
              <div className="flex justify-center mb-4">
                <div className="h-16 w-16 rounded-full bg-success/20 flex items-center justify-center">
                  <CheckCircle2 className="h-8 w-8 text-success" />
                </div>
              </div>
              <h1 className="text-2xl font-bold text-text-primary mb-2">Email Verified!</h1>
              <p className="text-text-secondary mb-6">
                Your email has been successfully verified. You can now access your account.
              </p>
              <Link href="/dashboard" className="btn btn-primary">
                Go to Dashboard
              </Link>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="text-center mb-8">
                <div className="flex justify-center mb-4">
                  <div className="h-16 w-16 rounded-full bg-gold/20 flex items-center justify-center">
                    <Mail className="h-8 w-8 text-gold" />
                  </div>
                </div>
                <h1 className="text-3xl font-bold text-text-primary mb-2">Verify Email</h1>
                <p className="text-text-secondary">
                  Enter the code sent to your email address
                </p>
              </div>

              <div>
                <label htmlFor="code" className="label">
                  Verification Code
                </label>
                <input
                  id="code"
                  type="text"
                  value={code}
                  onChange={(e) => setCode(e.target.value.toUpperCase())}
                  disabled={isLoading}
                  placeholder="000000"
                  maxLength={6}
                  className="input text-center tracking-widest text-2xl"
                />
              </div>

              <button
                type="submit"
                disabled={isLoading || code.length < 6}
                className="btn btn-primary w-full justify-center gap-2"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="h-5 w-5 animate-spin" />
                    Verifying...
                  </>
                ) : (
                  'Verify Email'
                )}
              </button>

              <p className="text-center text-sm text-text-secondary">
                Didn&apos;t receive the code?{' '}
                <button type="button" className="text-gold hover:text-gold-light transition-colors">
                  Resend
                </button>
              </p>
            </form>
          )}
        </motion.div>
      </div>
    </div>
  );
}
