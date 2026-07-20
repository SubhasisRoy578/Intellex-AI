// User types
export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  createdAt: Date;
  updatedAt: Date;
}

// Message types
export interface Message {
  id: string;
  conversationId: string;
  userId?: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  isStreaming?: boolean;
  error?: string;
  metadata?: {
    documentContext?: DocumentContext;
    imageContext?: ImageContext;
    webSearchQuery?: string;
  };
}

// Conversation types
export interface Conversation {
  id: string;
  userId: string;
  title: string;
  messages: Message[];
  documentContext?: DocumentContext;
  imageContext?: ImageContext;
  createdAt: Date;
  updatedAt: Date;
  lastMessageAt?: Date;
}

// Document context types
export interface DocumentContext {
  id: string;
  name: string;
  type: 'pdf' | 'docx' | 'txt';
  size: number;
  uploadedAt: Date;
  pages?: number;
  preview?: string;
}

// Image context types
export interface ImageContext {
  id: string;
  name: string;
  type: 'jpg' | 'jpeg' | 'png';
  size: number;
  uploadedAt: Date;
  preview: string;
  dimensions?: {
    width: number;
    height: number;
  };
}

// Upload types
export interface UploadProgress {
  isUploading: boolean;
  progress: number;
  fileName?: string;
  error?: string;
}

// Chat input types
export interface ChatInputState {
  message: string;
  isLoading: boolean;
  error?: string;
  attachments: (DocumentContext | ImageContext)[];
}

// Response streaming types
export interface StreamingMessage {
  id: string;
  content: string;
  isStreaming: boolean;
  timestamp: Date;
}

// File validation types
export interface FileValidationResult {
  valid: boolean;
  error?: string;
  file?: File;
  type?: 'document' | 'image';
}

// Auth form types
export interface AuthFormState {
  isLoading: boolean;
  error?: string;
  success?: boolean;
}

// Settings types
export interface UserSettings {
  userId: string;
  theme: 'dark' | 'light' | 'system';
  notifications: boolean;
  emailUpdates: boolean;
  privacyMode: boolean;
  autoSave: boolean;
  fontSize: 'small' | 'medium' | 'large';
}

// API response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}
