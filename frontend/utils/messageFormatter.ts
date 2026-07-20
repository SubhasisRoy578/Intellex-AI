import hljs from 'highlight.js';

export interface CodeBlock {
  language: string;
  code: string;
}

// Extract code blocks from message
export function extractCodeBlocks(content: string): CodeBlock[] {
  const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
  const blocks: CodeBlock[] = [];
  let match;

  while ((match = codeBlockRegex.exec(content)) !== null) {
    blocks.push({
      language: match[1] || 'text',
      code: match[2].trim(),
    });
  }

  return blocks;
}

// Highlight code with language support
export function highlightCode(code: string, language: string = 'text'): string {
  try {
    if (language === 'text' || language === 'plain') {
      return code;
    }

    // Check if language is supported by highlight.js
    const validLanguage = hljs.getLanguage(language) ? language : 'text';

    if (validLanguage === 'text') {
      return code;
    }

    return hljs.highlight(code, { language: validLanguage }).value;
  } catch (error) {
    console.error('[v0] Syntax highlighting error:', error);
    return code;
  }
}

// Format timestamp
export function formatTime(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  const now = new Date();
  const diff = now.getTime() - d.getTime();

  // Less than 1 minute
  if (diff < 60000) {
    return 'just now';
  }

  // Less than 1 hour
  if (diff < 3600000) {
    const minutes = Math.floor(diff / 60000);
    return `${minutes}m ago`;
  }

  // Less than 1 day
  if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000);
    return `${hours}h ago`;
  }

  // Same day (show time)
  if (d.toDateString() === now.toDateString()) {
    return d.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true,
    });
  }

  // Yesterday
  const yesterday = new Date(now);
  yesterday.setDate(yesterday.getDate() - 1);
  if (d.toDateString() === yesterday.toDateString()) {
    return 'Yesterday';
  }

  // Within a week
  if (diff < 604800000) {
    return d.toLocaleDateString('en-US', { weekday: 'short' });
  }

  // Default: show date
  return d.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
  });
}

// Format conversation title from first message
export function generateConversationTitle(firstMessage: string): string {
  // Remove markdown and special characters
  let title = firstMessage
    .replace(/[#*_~`]/g, '')
    .trim()
    .substring(0, 50);

  // Add ellipsis if truncated
  if (firstMessage.length > 50) {
    title += '...';
  }

  return title || 'New Conversation';
}

// Check if message contains code
export function hasCodeBlock(content: string): boolean {
  return /```[\s\S]*?```/g.test(content);
}

// Extract mention tags from content
export function extractMentions(content: string): string[] {
  const mentionRegex = /@(\w+)/g;
  const mentions: string[] = [];
  let match;

  while ((match = mentionRegex.exec(content)) !== null) {
    mentions.push(match[1]);
  }

  return [...new Set(mentions)];
}

// Check if content is a code-only message
export function isCodeOnlyMessage(content: string): boolean {
  const trimmed = content.trim();
  return (
    trimmed.startsWith('```') && trimmed.endsWith('```') && trimmed.split('```').length === 3
  );
}

// Parse markdown links
export function parseMarkdownLinks(content: string): Array<{ text: string; url: string }> {
  const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
  const links: Array<{ text: string; url: string }> = [];
  let match;

  while ((match = linkRegex.exec(content)) !== null) {
    links.push({
      text: match[1],
      url: match[2],
    });
  }

  return links;
}

// Truncate text with ellipsis
export function truncateText(text: string, maxLength: number = 100): string {
  if (text.length <= maxLength) {
    return text;
  }
  return text.substring(0, maxLength) + '...';
}

// Escape HTML special characters
export function escapeHtml(text: string): string {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Convert markdown to plain text (basic)
export function markdownToPlainText(markdown: string): string {
  return markdown
    .replace(/```[\s\S]*?```/g, '') // Remove code blocks
    .replace(/#+\s+/g, '') // Remove headings
    .replace(/[*_]/g, '') // Remove emphasis markers
    .replace(/\[([^\]]+)\]/g, '$1') // Remove link brackets
    .replace(/\n\n+/g, '\n') // Normalize line breaks
    .trim();
}
