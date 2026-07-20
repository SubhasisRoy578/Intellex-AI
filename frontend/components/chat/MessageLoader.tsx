'use client';

import { motion } from 'framer-motion';

export function MessageLoader() {
  return (
    <div className="flex gap-3 mb-4 animate-pulse">
      <div className="flex-shrink-0 h-8 w-8 rounded-lg bg-gold/20"></div>
      <div className="flex flex-col gap-2 max-w-xl flex-1">
        <div className="rounded-lg px-4 py-3 bg-surface border border-border space-y-2">
          <div className="h-4 bg-border rounded w-3/4"></div>
          <div className="h-4 bg-border rounded w-1/2"></div>
          <div className="h-4 bg-border rounded w-2/3"></div>
        </div>
        <div className="h-3 bg-border rounded w-20"></div>
      </div>
    </div>
  );
}
