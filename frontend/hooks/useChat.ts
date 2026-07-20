import { useState, useCallback } from 'react';
import type { Message, Conversation, DocumentContext, ImageContext } from '@/types';

interface UseChatOptions {
  initialConversationId?: string;
  onMessageSent?: (message: Message) => void;
  onError?: (error: Error) => void;
}

export function useChat(options?: UseChatOptions) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [currentConversationId] = useState(
    options?.initialConversationId || new Date().getTime().toString()
  );
  const [documentContext, setDocumentContext] = useState<DocumentContext | null>(null);
  const [imageContext, setImageContext] = useState<ImageContext | null>(null);

  const addMessage = useCallback(
    (content: string, role: 'user' | 'assistant' = 'user', metadata?: any) => {
      const message: Message = {
        id: Date.now().toString(),
        conversationId: currentConversationId,
        content,
        role,
        timestamp: new Date(),
        metadata: {
          documentContext: documentContext || undefined,
          imageContext: imageContext || undefined,
          ...metadata,
        },
      };

      setMessages((prev) => [...prev, message]);
      options?.onMessageSent?.(message);
      return message;
    },
    [currentConversationId, documentContext, imageContext, options]
  );

  const sendMessage = useCallback(
    async (message: string, files?: File[]) => {
      try {
        setError(null);
        setIsLoading(true);

        // Add user message
        addMessage(message, 'user');

        // Simulate API call delay
        await new Promise((resolve) => setTimeout(resolve, 800));

        // Add assistant response
        setIsStreaming(true);
        await new Promise((resolve) => setTimeout(resolve, 500));

        const responseContent = `I received your message: "${message}"${
          files?.length ? ` with ${files.length} file(s)` : ''
        }. In a real app, I would process this with an AI model.`;

        addMessage(responseContent, 'assistant');
        setIsStreaming(false);

        console.log('[v0] Message sent successfully');
      } catch (err) {
        const error = err instanceof Error ? err : new Error('Unknown error');
        setError(error);
        options?.onError?.(error);
        setIsStreaming(false);
      } finally {
        setIsLoading(false);
      }
    },
    [addMessage, options]
  );

  const setDocument = useCallback((document: DocumentContext | null) => {
    setDocumentContext(document);
  }, []);

  const setImage = useCallback((image: ImageContext | null) => {
    setImageContext(image);
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  const removeMessage = useCallback((messageId: string) => {
    setMessages((prev) => prev.filter((m) => m.id !== messageId));
  }, []);

  const updateMessage = useCallback((messageId: string, updates: Partial<Message>) => {
    setMessages((prev) =>
      prev.map((m) => (m.id === messageId ? { ...m, ...updates } : m))
    );
  }, []);

  return {
    messages,
    isLoading,
    isStreaming,
    error,
    currentConversationId,
    documentContext,
    imageContext,
    addMessage,
    sendMessage,
    setDocument,
    setImage,
    clearMessages,
    removeMessage,
    updateMessage,
  };
}
