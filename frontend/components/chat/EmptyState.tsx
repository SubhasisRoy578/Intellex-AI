'use client';

import { MessageSquare, Zap, FileText, ImageIcon } from 'lucide-react';
import { motion } from 'framer-motion';

interface EmptyStateProps {
  onSuggestionClick?: (suggestion: string) => void;
}

export function EmptyState({ onSuggestionClick }: EmptyStateProps) {
  const suggestions = [
    {
      icon: Zap,
      title: 'Analyze Code',
      description: 'Get code reviews and optimization tips',
    },
    {
      icon: FileText,
      title: 'Process Documents',
      description: 'Upload and analyze PDFs, DOCX, or TXT files',
    },
    {
      icon: ImageIcon,
      title: 'Understand Images',
      description: 'Upload images for AI analysis and insights',
    },
    {
      icon: MessageSquare,
      title: 'Ask Questions',
      description: 'Get comprehensive answers to any question',
    },
  ];

  return (
    <div className="flex flex-col items-center justify-center min-h-[500px] py-12 px-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.6 }}
        className="text-center mb-12"
      >
        <div className="flex justify-center mb-4">
          <div className="h-16 w-16 rounded-2xl bg-gradient-to-br from-gold to-amber flex items-center justify-center">
            <MessageSquare className="h-8 w-8 text-background" />
          </div>
        </div>

        <h1 className="text-3xl font-bold text-text-primary mb-2">Welcome to Intellex</h1>
        <p className="text-text-secondary max-w-md mx-auto">
          Start a new conversation or try one of the suggestions below to explore what Intellex can do
        </p>
      </motion.div>

      {/* Suggestions Grid */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 w-full max-w-2xl">
        {suggestions.map((suggestion, i) => (
          <motion.button
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: i * 0.1 }}
            onClick={() => onSuggestionClick?.(suggestion.title)}
            className="card text-left hover:border-gold/50 hover:bg-hover transition-all group cursor-pointer"
          >
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 h-10 w-10 rounded-lg bg-gold/10 flex items-center justify-center group-hover:bg-gold/20 transition-colors">
                <suggestion.icon className="h-5 w-5 text-gold" />
              </div>
              <div>
                <h3 className="font-semibold text-text-primary group-hover:text-gold transition-colors">
                  {suggestion.title}
                </h3>
                <p className="text-sm text-text-secondary mt-1">{suggestion.description}</p>
              </div>
            </div>
          </motion.button>
        ))}
      </div>

      {/* Tips */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="mt-12 p-6 rounded-lg bg-surface/50 border border-border max-w-2xl"
      >
        <h3 className="font-semibold text-text-primary mb-3">Tips for best results:</h3>
        <ul className="space-y-2 text-sm text-text-secondary">
          <li className="flex gap-2">
            <span className="text-gold">•</span>
            <span>Be specific with your questions for more accurate responses</span>
          </li>
          <li className="flex gap-2">
            <span className="text-gold">•</span>
            <span>Use Shift+Enter to create multi-line messages</span>
          </li>
          <li className="flex gap-2">
            <span className="text-gold">•</span>
            <span>Attach files for context-aware analysis</span>
          </li>
          <li className="flex gap-2">
            <span className="text-gold">•</span>
            <span>Ask follow-up questions to dig deeper</span>
          </li>
        </ul>
      </motion.div>
    </div>
  );
}
