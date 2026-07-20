'use client';

import { motion } from 'framer-motion';

export function TypingIndicator() {
  const containerVariants = {
    animate: {
      transition: {
        staggerChildren: 0.2,
      },
    },
  };

  const dotVariants = {
    initial: { y: 0, opacity: 0.5 },
    animate: {
      y: -10,
      opacity: 1,
      transition: {
        duration: 0.6,
        repeat: Infinity,
        repeatType: 'reverse' as const,
      },
    },
  };

  return (
    <div className="flex gap-2 items-center">
      <div className="flex-shrink-0 h-8 w-8 rounded-lg bg-gold/20 flex items-center justify-center">
        <span className="text-sm font-bold text-gold">AI</span>
      </div>

      <motion.div
        className="flex gap-1 px-4 py-3 rounded-lg bg-surface border border-border"
        variants={containerVariants}
        animate="animate"
      >
        {[0, 1, 2].map((i) => (
          <motion.div
            key={i}
            className="h-2 w-2 rounded-full bg-gold"
            variants={dotVariants}
          />
        ))}
      </motion.div>
    </div>
  );
}
