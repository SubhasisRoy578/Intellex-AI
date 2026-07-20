'use client';

import { AlertCircle, RotateCcw, X } from 'lucide-react';
import { motion } from 'framer-motion';

interface ErrorCardProps {
  title: string;
  message: string;
  onRetry?: () => void;
  onDismiss?: () => void;
  type?: 'error' | 'warning' | 'info';
}

export function ErrorCard({
  title,
  message,
  onRetry,
  onDismiss,
  type = 'error',
}: ErrorCardProps) {
  const colors = {
    error: {
      bg: 'bg-error/10',
      border: 'border-error/50',
      icon: 'text-error',
      button: 'bg-error/20 hover:bg-error/30 text-error',
    },
    warning: {
      bg: 'bg-warning/10',
      border: 'border-warning/50',
      icon: 'text-warning',
      button: 'bg-warning/20 hover:bg-warning/30 text-warning',
    },
    info: {
      bg: 'bg-info/10',
      border: 'border-info/50',
      icon: 'text-info',
      button: 'bg-info/20 hover:bg-info/30 text-info',
    },
  };

  const color = colors[type];

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.3 }}
      className={`rounded-lg border ${color.border} ${color.bg} p-4`}
    >
      <div className="flex gap-4">
        {/* Icon */}
        <div className="flex-shrink-0 mt-0.5">
          <AlertCircle className={`h-5 w-5 ${color.icon}`} />
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <h3 className={`font-semibold ${color.icon}`}>{title}</h3>
          <p className="text-sm text-text-secondary mt-1">{message}</p>

          {/* Action Buttons */}
          {(onRetry || onDismiss) && (
            <div className="flex gap-2 mt-4">
              {onRetry && (
                <button
                  onClick={onRetry}
                  className={`flex items-center gap-2 px-3 py-1.5 text-sm rounded-lg transition-colors ${color.button}`}
                >
                  <RotateCcw className="h-4 w-4" />
                  Try Again
                </button>
              )}
              {onDismiss && (
                <button
                  onClick={onDismiss}
                  className="flex items-center gap-2 px-3 py-1.5 text-sm rounded-lg bg-text-tertiary/20 hover:bg-text-tertiary/30 text-text-secondary transition-colors"
                >
                  <X className="h-4 w-4" />
                  Dismiss
                </button>
              )}
            </div>
          )}
        </div>

        {/* Close Button */}
        {onDismiss && !onRetry && (
          <button
            onClick={onDismiss}
            className="flex-shrink-0 text-text-tertiary hover:text-text-secondary transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        )}
      </div>
    </motion.div>
  );
}
