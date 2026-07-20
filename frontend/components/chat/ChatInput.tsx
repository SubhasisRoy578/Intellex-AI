'use client';

import { Send, Paperclip, X } from 'lucide-react';
import { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { validateFile } from '@/utils/fileValidator';

interface ChatInputProps {
  isLoading?: boolean;
  onSubmit?: (message: string, files?: File[]) => void;
  placeholder?: string;
  disabled?: boolean;
}

export function ChatInput({
  isLoading = false,
  onSubmit,
  placeholder = 'Type your message here...',
  disabled = false,
}: ChatInputProps) {
  const [input, setInput] = useState('');
  const [attachedFiles, setAttachedFiles] = useState<File[]>([]);
  const [error, setError] = useState<string>();
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim() && attachedFiles.length === 0) {
      return;
    }

    // Check for IME composition
    if ((e as any).nativeEvent?.isComposing) {
      return;
    }

    onSubmit?.(input, attachedFiles.length > 0 ? attachedFiles : undefined);
    setInput('');
    setAttachedFiles([]);
    setError(undefined);

    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Don't submit on IME composition
    if ((e as any).nativeEvent?.isComposing || e.keyCode === 229) {
      return;
    }

    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any);
    }
  };

  const handleFileSelect = (files: FileList | null) => {
    if (!files) return;

    const newFiles: File[] = [];
    const errors: string[] = [];

    Array.from(files).forEach((file) => {
      const validation = validateFile(file);

      if (validation.valid && validation.file) {
        newFiles.push(validation.file);
      } else {
        errors.push(validation.error || 'Unknown error');
      }
    });

    if (errors.length > 0) {
      setError(errors[0]);
      setTimeout(() => setError(undefined), 5000);
    }

    if (newFiles.length > 0) {
      setAttachedFiles((prev) => [...prev, ...newFiles].slice(0, 3)); // Max 3 files
    }
  };

  const handleAttachClick = () => {
    fileInputRef.current?.click();
  };

  const removeFile = (index: number) => {
    setAttachedFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);

    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 150) + 'px';
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      {/* Error message */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          className="mb-3 rounded-lg border border-error/50 bg-error/10 px-4 py-2 text-sm text-error"
        >
          {error}
        </motion.div>
      )}

      {/* Attached files preview */}
      {attachedFiles.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-3 flex flex-wrap gap-2"
        >
          {attachedFiles.map((file, index) => (
            <div
              key={index}
              className="flex items-center gap-2 rounded-lg border border-gold/50 bg-gold/10 px-3 py-2"
            >
              <span className="text-sm text-text-secondary truncate max-w-xs">
                {file.name}
              </span>
              <button
                type="button"
                onClick={() => removeFile(index)}
                className="text-text-tertiary hover:text-error transition-colors"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          ))}
        </motion.div>
      )}

      {/* Input area */}
      <div className="flex gap-3 rounded-lg border border-border bg-surface p-3 focus-within:ring-2 focus-within:ring-gold focus-within:border-transparent transition-all">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={handleTextareaChange}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled || isLoading}
          rows={1}
          className="flex-1 resize-none bg-transparent text-text-primary placeholder-text-tertiary focus:outline-none"
        />

        <div className="flex items-end gap-2">
          <button
            type="button"
            onClick={handleAttachClick}
            disabled={disabled || isLoading || attachedFiles.length >= 3}
            className="flex-shrink-0 text-text-secondary hover:text-gold disabled:text-text-tertiary disabled:cursor-not-allowed transition-colors"
            title="Attach file (PDF, DOCX, TXT, JPG, PNG)"
          >
            <Paperclip className="h-5 w-5" />
          </button>

          <button
            type="submit"
            disabled={disabled || isLoading || (!input.trim() && attachedFiles.length === 0)}
            className="flex-shrink-0 rounded-lg bg-gold p-2 text-background hover:bg-gold-light disabled:bg-disabled disabled:cursor-not-allowed transition-colors"
          >
            <Send className="h-5 w-5" />
          </button>
        </div>
      </div>

      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept=".pdf,.docx,.txt,.jpg,.jpeg,.png"
        onChange={(e) => handleFileSelect(e.target.files)}
        className="hidden"
        aria-label="Attach files"
      />

      <p className="mt-2 text-xs text-text-tertiary">
        Use Shift+Enter for new line • Supports PDF, DOCX, TXT, JPG, PNG
      </p>
    </form>
  );
}
