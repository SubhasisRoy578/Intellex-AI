'use client';

import { motion } from 'framer-motion';
import { Settings, Bell, Lock, Zap } from 'lucide-react';

export default function SettingsPage() {
  const settings = [
    {
      icon: Bell,
      title: 'Notifications',
      description: 'Manage your notification preferences',
    },
    {
      icon: Lock,
      title: 'Privacy & Security',
      description: 'Control your privacy and security settings',
    },
    {
      icon: Zap,
      title: 'Preferences',
      description: 'Customize your Intellex experience',
    },
  ];

  return (
    <div className="p-6 sm:p-8 max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="flex items-center gap-3 mb-8">
          <Settings className="h-8 w-8 text-gold" />
          <h1 className="text-3xl font-bold text-text-primary">Settings</h1>
        </div>

        <div className="space-y-4">
          {settings.map((setting, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: i * 0.1 }}
              className="card hover:border-gold/50 cursor-pointer transition-all"
            >
              <div className="flex items-start gap-4">
                <div className="h-12 w-12 rounded-lg bg-gold/10 flex items-center justify-center flex-shrink-0">
                  <setting.icon className="h-6 w-6 text-gold" />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-text-primary">{setting.title}</h3>
                  <p className="text-sm text-text-secondary mt-1">{setting.description}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Danger Zone */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-12 p-6 rounded-lg border border-error/50 bg-error/10"
        >
          <h3 className="font-semibold text-error mb-4">Danger Zone</h3>
          <button className="btn bg-error text-white hover:bg-red-600">
            Delete Account
          </button>
        </motion.div>
      </motion.div>
    </div>
  );
}
