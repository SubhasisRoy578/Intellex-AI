import { useState, useCallback } from 'react';
import type { Conversation } from '@/types';

interface UseConversationsOptions {
  onConversationCreated?: (conversation: Conversation) => void;
  onConversationDeleted?: (conversationId: string) => void;
}

export function useConversations(options?: UseConversationsOptions) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const createConversation = useCallback(
    async (title: string) => {
      try {
        setError(null);
        setIsLoading(true);

        const newConversation: Conversation = {
          id: Date.now().toString(),
          userId: 'user-1', // Would come from auth
          title,
          messages: [],
          createdAt: new Date(),
          updatedAt: new Date(),
        };

        setConversations((prev) => [newConversation, ...prev]);
        setCurrentConversationId(newConversation.id);
        options?.onConversationCreated?.(newConversation);

        console.log('[v0] Conversation created:', newConversation.id);
        return newConversation;
      } catch (err) {
        const error = err instanceof Error ? err : new Error('Failed to create conversation');
        setError(error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    [options]
  );

  const deleteConversation = useCallback(
    async (conversationId: string) => {
      try {
        setError(null);
        setIsLoading(true);

        setConversations((prev) =>
          prev.filter((c) => c.id !== conversationId)
        );

        if (currentConversationId === conversationId) {
          setCurrentConversationId(null);
        }

        options?.onConversationDeleted?.(conversationId);
        console.log('[v0] Conversation deleted:', conversationId);
      } catch (err) {
        const error = err instanceof Error ? err : new Error('Failed to delete conversation');
        setError(error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    [currentConversationId, options]
  );

  const updateConversation = useCallback(
    (conversationId: string, updates: Partial<Conversation>) => {
      setConversations((prev) =>
        prev.map((c) =>
          c.id === conversationId
            ? { ...c, ...updates, updatedAt: new Date() }
            : c
        )
      );
    },
    []
  );

  const renameConversation = useCallback(
    (conversationId: string, newTitle: string) => {
      updateConversation(conversationId, { title: newTitle });
    },
    [updateConversation]
  );

  const getConversation = useCallback(
    (conversationId: string) => {
      return conversations.find((c) => c.id === conversationId);
    },
    [conversations]
  );

  const getCurrentConversation = useCallback(() => {
    if (!currentConversationId) return null;
    return getConversation(currentConversationId);
  }, [currentConversationId, getConversation]);

  const selectConversation = useCallback((conversationId: string) => {
    setCurrentConversationId(conversationId);
  }, []);

  const clearConversations = useCallback(() => {
    setConversations([]);
    setCurrentConversationId(null);
  }, []);

  return {
    conversations,
    currentConversationId,
    isLoading,
    error,
    createConversation,
    deleteConversation,
    updateConversation,
    renameConversation,
    getConversation,
    getCurrentConversation,
    selectConversation,
    clearConversations,
  };
}
