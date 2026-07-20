'use client';

import Link from 'next/link';
import { Navbar } from '@/components/layout/Navbar';
import { ArrowRight, Zap, Brain, FileText, ImageIcon } from 'lucide-react';
import { motion } from 'framer-motion';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background text-text-primary">
      <Navbar />

      {/* Hero Section */}
      <section className="relative overflow-hidden px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-4xl">
          {/* Animated background gradient */}
          <div className="absolute inset-0 -top-40 -z-10 opacity-20">
            <div className="absolute h-96 w-96 rounded-full bg-gold blur-3xl"></div>
            <div className="absolute right-0 top-40 h-96 w-96 rounded-full bg-amber blur-3xl"></div>
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center"
          >
            <h1 className="text-4xl font-bold sm:text-5xl md:text-6xl leading-tight mb-6">
              The Future of{' '}
              <span className="gradient-gold">Intelligent Conversations</span>
            </h1>

            <p className="mx-auto max-w-2xl text-lg text-text-secondary mb-8">
              Intellex AI brings premium artificial intelligence to your workflows. Chat with advanced AI,
              analyze documents, process images, and unlock insights like never before.
            </p>

            <div className="flex flex-col gap-4 sm:flex-row items-center justify-center mb-12">
              <Link
                href="/auth/sign-in"
                className="btn btn-primary text-base sm:text-lg inline-flex gap-2"
              >
                Get Started
                <ArrowRight className="h-5 w-5" />
              </Link>

              <Link
                href="#features"
                className="btn btn-secondary text-base sm:text-lg"
              >
                Learn More
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="relative px-4 py-20 sm:px-6 lg:px-8 bg-surface/20">
        <div className="mx-auto max-w-6xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-16 text-center"
          >
            <h2 className="text-3xl font-bold sm:text-4xl mb-4">Powerful Features</h2>
            <p className="max-w-2xl mx-auto text-text-secondary text-lg">
              Everything you need for premium AI interactions
            </p>
          </motion.div>

          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
            {[
              {
                icon: Brain,
                title: 'Advanced AI',
                description: 'State-of-the-art AI for intelligent conversations',
              },
              {
                icon: FileText,
                title: 'Document Analysis',
                description: 'Process PDF, DOCX, and TXT files',
              },
              {
                icon: ImageIcon,
                title: 'Image Processing',
                description: 'Analyze and understand images instantly',
              },
              {
                icon: Zap,
                title: 'Lightning Fast',
                description: 'Real-time responses and instant results',
              },
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: i * 0.1 }}
                className="card"
              >
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-gold/10">
                  <feature.icon className="h-6 w-6 text-gold" />
                </div>
                <h3 className="mb-2 font-semibold text-text-primary">{feature.title}</h3>
                <p className="text-sm text-text-secondary">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-4xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl font-bold sm:text-4xl mb-6">Ready to Experience Intellex?</h2>
            <p className="mb-8 text-lg text-text-secondary">
              Join thousands of users leveraging AI for productivity and insights.
            </p>
            <Link href="/auth/sign-up" className="btn btn-primary text-lg inline-flex gap-2">
              Start Free Trial
              <ArrowRight className="h-5 w-5" />
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border bg-surface/50 px-4 py-12 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-6xl">
          <div className="mb-8 grid grid-cols-2 gap-8 md:grid-cols-4">
            <div>
              <h4 className="mb-4 font-semibold text-text-primary">Product</h4>
              <ul className="space-y-2 text-sm text-text-secondary">
                <li><Link href="#" className="hover:text-gold transition-colors">Features</Link></li>
                <li><Link href="#" className="hover:text-gold transition-colors">Pricing</Link></li>
                <li><Link href="#" className="hover:text-gold transition-colors">Security</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="mb-4 font-semibold text-text-primary">Company</h4>
              <ul className="space-y-2 text-sm text-text-secondary">
                <li><Link href="#" className="hover:text-gold transition-colors">About</Link></li>
                <li><Link href="#" className="hover:text-gold transition-colors">Blog</Link></li>
                <li><Link href="#" className="hover:text-gold transition-colors">Careers</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="mb-4 font-semibold text-text-primary">Legal</h4>
              <ul className="space-y-2 text-sm text-text-secondary">
                <li><Link href="#" className="hover:text-gold transition-colors">Privacy</Link></li>
                <li><Link href="#" className="hover:text-gold transition-colors">Terms</Link></li>
                <li><Link href="#" className="hover:text-gold transition-colors">Contact</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="mb-4 font-semibold text-text-primary">Connect</h4>
              <ul className="space-y-2 text-sm text-text-secondary">
                <li><Link href="#" className="hover:text-gold transition-colors">Twitter</Link></li>
                <li><Link href="#" className="hover:text-gold transition-colors">GitHub</Link></li>
                <li><Link href="#" className="hover:text-gold transition-colors">Discord</Link></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-border pt-8 text-center text-sm text-text-tertiary">
            <p>&copy; 2024 Intellex AI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
