'use client';

import { Plus, MessageSquare, Settings, LogOut, ChevronDown } from 'lucide-react';
import Link from 'next/link';
import { useState } from 'react';
import { motion } from 'framer-motion';

interface SidebarProps {
  isOpen?: boolean;
  conversations?: Array<{
    id: string;
    title: string;
    lastMessageAt?: Date;
  }>;
  currentConversationId?: string;
  onNewConversation?: () => void;
}

export function Sidebar({
  isOpen = true,
  conversations = [],
  currentConversationId,
  onNewConversation,
}: SidebarProps) {
  const [isExpanded, setIsExpanded] = useState(true);

  if (!isOpen) {
    return null;
  }

  return (
    <motion.aside
      initial={{ x: -250 }}
      animate={{ x: 0 }}
      className="hidden md:flex flex-col w-64 border-r border-border bg-surface/50 h-screen"
    >
      {/* Header */}
      <div className="flex-shrink-0 p-4 border-b border-border">
        <button
          onClick={onNewConversation}
          className="w-full flex items-center justify-center gap-2 rounded-lg bg-gold text-background font-medium py-2 px-4 hover:bg-gold-light transition-colors"
        >
          <Plus className="h-4 w-4" />
          New Chat
        </button>
      </div>

      {/* Conversations List */}
      <div className="flex-1 overflow-y-auto px-3 py-4">
        <div className="mb-4">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="flex items-center gap-2 text-xs font-semibold text-text-tertiary hover:text-text-secondary transition-colors mb-2"
          >
            <ChevronDown
              className={`h-3 w-3 transition-transform ${isExpanded ? 'rotate-0' : '-rotate-90'}`}
            />
            RECENT
          </button>

          {isExpanded && (
            <div className="space-y-2">
              {conversations.length > 0 ? (
                conversations.map((conv) => (
                  <Link
                    key={conv.id}
                    href={`/dashboard?conversation=${conv.id}`}
                    className={`block truncate rounded-lg px-3 py-2 text-sm transition-all ${
                      currentConversationId === conv.id
                        ? 'bg-gold/20 text-gold border border-gold/50'
                        : 'text-text-secondary hover:bg-hover hover:text-text-primary'
                    }`}
                  >
                    {conv.title}
                  </Link>
                ))
              ) : (
                <p className="text-xs text-text-tertiary py-2">No conversations yet</p>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="flex-shrink-0 space-y-2 border-t border-border p-4">
        <Link
          href="/dashboard/settings"
          className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-text-secondary hover:bg-hover hover:text-text-primary transition-all"
        >
          <Settings className="h-4 w-4" />
          Settings
        </Link>
        <button className="w-full flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-text-secondary hover:bg-hover hover:text-error transition-all">
          <LogOut className="h-4 w-4" />
          Sign Out
        </button>
      </div>
    </motion.aside>
  );
}
