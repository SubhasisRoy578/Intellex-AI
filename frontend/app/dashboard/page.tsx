'use client';

import { useState, useRef, useEffect } from 'react';
import { MessageBubble } from '@/components/chat/MessageBubble';
import { ChatInput } from '@/components/chat/ChatInput';
import { EmptyState } from '@/components/chat/EmptyState';
import { TypingIndicator } from '@/components/chat/TypingIndicator';
import { MessageLoader } from '@/components/chat/MessageLoader';
import type { Message } from '@/types';

export default function DashboardPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isStreaming]);

  const handleSendMessage = async (message: string, files?: File[]) => {
    if (!message.trim() && !files?.length) {
      return;
    }

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      conversationId: '1',
      content: message,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    // Simulate streaming response
    try {
      // In a real app, this would call your API
      await new Promise((resolve) => setTimeout(resolve, 800));

      // Add assistant response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        conversationId: '1',
        content: `Thanks for your message! I'm a demo AI assistant. In a real implementation, I would:\n\n\`\`\`python\n# Process your message with advanced AI\nresponse = ai_model.generate(message)\nreturn response\n\`\`\`\n\nFeel free to:\n- Ask follow-up questions\n- Upload documents (PDF, DOCX, TXT)\n- Share images (JPG, PNG)\n\nHow can I help you today?`,
        role: 'assistant',
        timestamp: new Date(),
      };

      // Simulate streaming by adding message after a slight delay
      setIsStreaming(true);
      await new Promise((resolve) => setTimeout(resolve, 500));
      setMessages((prev) => [...prev, assistantMessage]);
      setIsStreaming(false);

      console.log('[v0] Message sent:', { userMessage, files: files?.map((f) => f.name) });
    } catch (error) {
      console.error('[v0] Error sending message:', error);
      setIsStreaming(false);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    handleSendMessage(suggestion);
  };

  return (
    <div className="flex flex-col h-full bg-background">
      {/* Chat Messages Area */}
      <div className="flex-1 overflow-y-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto">
          {/* Empty State or Messages */}
          {messages.length === 0 ? (
            <EmptyState onSuggestionClick={handleSuggestionClick} />
          ) : (
            <div>
              {messages.map((message) => (
                <MessageBubble
                  key={message.id}
                  content={message.content}
                  role={message.role}
                  timestamp={message.timestamp}
                />
              ))}

              {/* Loading State */}
              {isLoading && (
                <>
                  {isStreaming ? (
                    <TypingIndicator />
                  ) : (
                    <MessageLoader />
                  )}
                </>
              )}

              {/* Scroll anchor */}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </div>

      {/* Chat Input Area */}
      <div className="flex-shrink-0 border-t border-border bg-surface/50 backdrop-blur-sm px-4 py-6 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto">
          <ChatInput
            isLoading={isLoading}
            onSubmit={handleSendMessage}
            disabled={isStreaming}
          />
        </div>
      </div>
    </div>
  );
}
