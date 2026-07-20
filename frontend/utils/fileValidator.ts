import { FileValidationResult } from '@/types';

// Supported file types
const SUPPORTED_DOCUMENTS = ['pdf', 'docx', 'txt'];
const SUPPORTED_IMAGES = ['jpg', 'jpeg', 'png'];
const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB

export function validateFile(file: File): FileValidationResult {
  // Check file size
  if (file.size > MAX_FILE_SIZE) {
    return {
      valid: false,
      error: `File size exceeds ${MAX_FILE_SIZE / 1024 / 1024}MB limit`,
    };
  }

  // Get file extension
  const extension = file.name.split('.').pop()?.toLowerCase();

  if (!extension) {
    return {
      valid: false,
      error: 'File has no extension',
    };
  }

  // Check if document
  if (SUPPORTED_DOCUMENTS.includes(extension)) {
    return {
      valid: true,
      file,
      type: 'document',
    };
  }

  // Check if image
  if (SUPPORTED_IMAGES.includes(extension)) {
    return {
      valid: true,
      file,
      type: 'image',
    };
  }

  return {
    valid: false,
    error: `File type .${extension} is not supported. Supported formats: ${[...SUPPORTED_DOCUMENTS, ...SUPPORTED_IMAGES].join(', ')}`,
  };
}

export function getFileIcon(fileName: string): string {
  const extension = fileName.split('.').pop()?.toLowerCase();

  const iconMap: { [key: string]: string } = {
    pdf: 'FileText',
    docx: 'File',
    txt: 'FileText',
    jpg: 'Image',
    jpeg: 'Image',
    png: 'Image',
  };

  return iconMap[extension || ''] || 'File';
}

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

export function getFileType(fileName: string): 'document' | 'image' | 'unknown' {
  const extension = fileName.split('.').pop()?.toLowerCase();

  if (!extension) return 'unknown';

  if (SUPPORTED_DOCUMENTS.includes(extension)) return 'document';
  if (SUPPORTED_IMAGES.includes(extension)) return 'image';

  return 'unknown';
}
