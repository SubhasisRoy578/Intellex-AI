'use client';

import { X, Maximize2 } from 'lucide-react';
import type { ImageContext } from '@/types';
import { motion } from 'framer-motion';
import { useState } from 'react';

interface ImagePreviewProps {
  image: ImageContext;
  onRemove?: () => void;
  isActive?: boolean;
}

export function ImagePreview({
  image,
  onRemove,
  isActive = false,
}: ImagePreviewProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <>
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className={`rounded-lg border-2 p-2 transition-all overflow-hidden ${
          isActive
            ? 'border-gold bg-gold/10'
            : 'border-border bg-surface hover:border-gold/50'
        }`}
      >
        <div className="relative group">
          {/* Image Thumbnail */}
          <img
            src={image.preview}
            alt={image.name}
            className="w-full h-32 object-cover rounded-lg"
          />

          {/* Overlay Actions */}
          <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity rounded-lg flex items-center justify-center gap-2">
            <button
              onClick={() => setIsExpanded(true)}
              className="p-2 rounded-lg bg-gold/20 hover:bg-gold/30 text-gold transition-colors"
              title="Expand"
            >
              <Maximize2 className="h-5 w-5" />
            </button>
            <button
              onClick={onRemove}
              className="p-2 rounded-lg bg-error/20 hover:bg-error/30 text-error transition-colors"
              title="Remove"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Image Info */}
          <div className="mt-2 px-1">
            <p className="text-xs font-medium text-text-primary truncate">{image.name}</p>
            {image.dimensions && (
              <p className="text-xs text-text-tertiary">
                {image.dimensions.width}×{image.dimensions.height}
              </p>
            )}
          </div>

          {isActive && (
            <div className="mt-2 px-1 pt-2 border-t border-gold/20">
              <p className="text-xs text-gold font-medium">Active context</p>
            </div>
          )}
        </div>
      </motion.div>

      {/* Expanded View Modal */}
      {isExpanded && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={() => setIsExpanded(false)}
          className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        >
          <motion.div
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            exit={{ scale: 0.9 }}
            onClick={(e) => e.stopPropagation()}
            className="max-w-4xl w-full"
          >
            <img
              src={image.preview}
              alt={image.name}
              className="w-full h-auto rounded-lg max-h-[90vh] object-contain"
            />
            <button
              onClick={() => setIsExpanded(false)}
              className="absolute top-4 right-4 p-2 rounded-lg bg-background/80 hover:bg-background text-text-primary transition-colors"
            >
              <X className="h-6 w-6" />
            </button>
          </motion.div>
        </motion.div>
      )}
    </>
  );
}
