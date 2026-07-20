'use client';

import { FileText, X, Download } from 'lucide-react';
import type { DocumentContext } from '@/types';
import { formatFileSize } from '@/utils/fileValidator';
import { motion } from 'framer-motion';

interface DocumentCardProps {
  document: DocumentContext;
  onRemove?: () => void;
  onDownload?: () => void;
  isActive?: boolean;
}

export function DocumentCard({
  document,
  onRemove,
  onDownload,
  isActive = false,
}: DocumentCardProps) {
  const getFileIcon = (type: string) => {
    const icons: { [key: string]: string } = {
      pdf: '📄',
      docx: '📝',
      txt: '📋',
    };
    return icons[type] || '📎';
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className={`rounded-lg border-2 p-4 transition-all ${
        isActive
          ? 'border-gold bg-gold/10'
          : 'border-border bg-surface hover:border-gold/50'
      }`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3 flex-1 min-w-0">
          <span className="text-2xl flex-shrink-0">{getFileIcon(document.type)}</span>
          <div className="min-w-0">
            <p className="font-medium text-text-primary truncate">{document.name}</p>
            <p className="text-xs text-text-tertiary mt-1">
              {formatFileSize(document.size)} • {document.pages ? `${document.pages} pages` : document.type.toUpperCase()}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-1 flex-shrink-0">
          <button
            onClick={onDownload}
            className="p-1.5 rounded-lg hover:bg-hover text-text-tertiary hover:text-gold transition-colors"
            title="Download"
          >
            <Download className="h-4 w-4" />
          </button>
          <button
            onClick={onRemove}
            className="p-1.5 rounded-lg hover:bg-error/10 text-text-tertiary hover:text-error transition-colors"
            title="Remove"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      </div>

      {isActive && (
        <div className="mt-3 pt-3 border-t border-gold/20">
          <p className="text-xs text-gold font-medium">Active context</p>
        </div>
      )}
    </motion.div>
  );
}
