'use client';

import { motion } from 'framer-motion';
import { User, Mail, Calendar, Edit2 } from 'lucide-react';

export default function ProfilePage() {
  return (
    <div className="p-6 sm:p-8 max-w-2xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* Profile Header */}
        <div className="card mb-6">
          <div className="flex items-start justify-between mb-6">
            <div className="flex items-start gap-4">
              <div className="h-16 w-16 rounded-full bg-gradient-to-br from-gold to-amber flex items-center justify-center">
                <User className="h-8 w-8 text-background" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-text-primary">John Doe</h1>
                <p className="text-text-secondary">Premium Member</p>
              </div>
            </div>
            <button className="btn btn-secondary btn-sm flex items-center gap-2">
              <Edit2 className="h-4 w-4" />
              Edit
            </button>
          </div>
        </div>

        {/* Profile Information */}
        <div className="space-y-4 mb-8">
          {[
            { icon: Mail, label: 'Email', value: 'john@example.com' },
            { icon: User, label: 'Full Name', value: 'John Doe' },
            { icon: Calendar, label: 'Member Since', value: 'January 15, 2024' },
          ].map((item, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: i * 0.1 }}
              className="card"
            >
              <div className="flex items-center gap-4">
                <div className="h-10 w-10 rounded-lg bg-gold/10 flex items-center justify-center flex-shrink-0">
                  <item.icon className="h-5 w-5 text-gold" />
                </div>
                <div>
                  <p className="text-sm text-text-tertiary">{item.label}</p>
                  <p className="font-medium text-text-primary">{item.value}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Statistics */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="grid grid-cols-3 gap-4"
        >
          {[
            { label: 'Conversations', value: '12' },
            { label: 'Messages', value: '156' },
            { label: 'Files Analyzed', value: '28' },
          ].map((stat, i) => (
            <div
              key={i}
              className="card text-center"
            >
              <p className="text-2xl font-bold text-gold">{stat.value}</p>
              <p className="text-sm text-text-secondary mt-1">{stat.label}</p>
            </div>
          ))}
        </motion.div>
      </motion.div>
    </div>
  );
}
