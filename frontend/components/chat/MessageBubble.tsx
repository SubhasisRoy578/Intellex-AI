'use client';

import { Copy, Check } from 'lucide-react';
import { useState } from 'react';
import { motion } from 'framer-motion';
import { formatTime, hasCodeBlock, extractCodeBlocks, highlightCode } from '@/utils/messageFormatter';
import Markdown from 'react-markdown';
import hljs from 'highlight.js';
import 'highlight.js/styles/atom-one-dark.css';

interface MessageBubbleProps {
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date | string;
  isStreaming?: boolean;
}

export function MessageBubble({
  content,
  role,
  timestamp,
  isStreaming = false,
}: MessageBubbleProps) {
  const [copied, setCopied] = useState(false);
  const isUser = role === 'user';

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('[v0] Failed to copy:', err);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex gap-3 mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      {/* Assistant Avatar */}
      {!isUser && (
        <div className="flex-shrink-0 h-8 w-8 rounded-lg bg-gold/20 flex items-center justify-center">
          <span className="text-sm font-bold text-gold">AI</span>
        </div>
      )}

      {/* Message Content */}
      <div className={`flex flex-col gap-2 max-w-xl ${isUser ? 'items-end' : 'items-start'}`}>
        <div
          className={`rounded-lg px-4 py-3 ${
            isUser
              ? 'bg-gold text-background rounded-br-none'
              : 'bg-surface border border-border text-text-primary rounded-bl-none'
          } ${isStreaming ? 'animate-pulse' : ''}`}
        >
          <Markdown
            components={{
              p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
              a: ({ href, children }) => (
                <a
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`underline ${
                    isUser
                      ? 'text-background/80 hover:text-background'
                      : 'text-gold hover:text-gold-light'
                  }`}
                >
                  {children}
                </a>
              ),
              code: ({ inline, children, className }) => {
                if (inline) {
                  return (
                    <code
                      className={`rounded px-1.5 py-0.5 font-mono text-xs ${
                        isUser
                          ? 'bg-background/20 text-background'
                          : 'bg-gold/10 text-amber'
                      }`}
                    >
                      {children}
                    </code>
                  );
                }
                return null;
              },
              pre: ({ children }) => (
                <pre className="rounded-lg bg-black/50 p-3 overflow-x-auto my-2">
                  {children}
                </pre>
              ),
              ul: ({ children }) => (
                <ul className="list-disc list-inside my-2 space-y-1">{children}</ul>
              ),
              ol: ({ children }) => (
                <ol className="list-decimal list-inside my-2 space-y-1">{children}</ol>
              ),
              blockquote: ({ children }) => (
                <blockquote className={`border-l-4 pl-3 my-2 italic ${
                  isUser ? 'border-background/50' : 'border-gold/50'
                }`}>
                  {children}
                </blockquote>
              ),
            }}
          >
            {content}
          </Markdown>
        </div>

        {/* Time and Actions */}
        <div className={`flex items-center gap-2 text-xs text-text-tertiary ${isUser ? 'flex-row-reverse' : ''}`}>
          <span>{formatTime(timestamp)}</span>

          {hasCodeBlock(content) && !isUser && (
            <button
              onClick={handleCopy}
              className="flex items-center gap-1 rounded px-2 py-1 hover:bg-hover transition-colors"
              title="Copy code"
            >
              {copied ? (
                <Check className="h-3 w-3 text-success" />
              ) : (
                <Copy className="h-3 w-3 text-text-tertiary hover:text-gold" />
              )}
            </button>
          )}
        </div>
      </div>

      {/* User Avatar */}
      {isUser && (
        <div className="flex-shrink-0 h-8 w-8 rounded-lg bg-gold flex items-center justify-center">
          <span className="text-sm font-bold text-background">U</span>
        </div>
      )}
    </motion.div>
  );
}
