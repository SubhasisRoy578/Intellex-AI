# Intellex AI - Premium AI Frontend

A production-ready, enterprise-grade AI SaaS frontend built with Next.js 16, React 19, and TypeScript.

## Project Structure

```
frontend/
├── app/                      # Next.js app directory
│   ├── (landing)/           # Landing page route
│   ├── auth/                # Authentication pages
│   │   ├── sign-in/
│   │   ├── sign-up/
│   │   ├── forgot-password/
│   │   └── verify-email/
│   ├── dashboard/           # Dashboard pages
│   │   ├── settings/
│   │   ├── profile/
│   │   └── page.tsx         # Main chat interface
│   ├── layout.tsx           # Root layout
│   ├── globals.css          # Global styles & theme
│   └── page.tsx             # Landing page
├── components/              # React components
│   ├── layout/             # Layout components (Navbar, Sidebar)
│   ├── auth/               # Authentication forms
│   ├── chat/               # Chat interface components
│   └── ui/                 # UI components
├── hooks/                  # Custom React hooks
│   ├── useChat.ts          # Chat state management
│   └── useConversations.ts # Conversation management
├── lib/                    # Utilities & helpers
│   └── theme.ts            # Design tokens
├── types/                  # TypeScript types
│   └── index.ts            # Shared types
├── utils/                  # Helper functions
│   ├── fileValidator.ts    # File upload validation
│   └── messageFormatter.ts # Message formatting & rendering
└── public/                 # Static assets
```

## Design System

### Premium Dark Gold Theme
- **Background**: `#0a0a0a` (near black)
- **Surface**: `#141414` (dark gray)
- **Card**: `#1b1b1b` (slightly lighter)
- **Gold Accent**: `#d4af37` (premium gold)
- **Text Primary**: `#ffffff` (white)

### Color Palette
- Gold: Primary accent for CTAs and highlights
- Amber: Secondary accent for code/highlights
- Success: `#10b981` (green)
- Error: `#ef4444` (red)
- Warning: `#f59e0b` (amber)
- Info: `#3b82f6` (blue)

### Typography
- **Font**: System UI with fallbacks (Geist from Google Fonts)
- **Sizes**: xs (12px) → 5xl (48px)
- **Line Heights**: 1.2 (tight) → 1.8 (loose)
- **Weights**: 300 (light) → 800 (extrabold)

## Features

### 1. Landing Page
- Hero section with gradient text
- Feature showcase with 4 core capabilities
- CTA section with premium styling
- Footer with links and copyright

### 2. Authentication System
- Sign In page with email/password validation
- Sign Up page with form validation
- Forgot Password recovery flow
- Email verification page

### 3. Chat Dashboard
- Premium chat interface with message history
- Sidebar with conversation management
- Empty state with suggestion cards
- Real-time message display with streaming animations

### 4. File Upload System
- Support for: PDF, DOCX, TXT (documents), JPG, PNG (images)
- File validation with error handling
- Progress indicators and feedback
- Document card and image preview components

### 5. User Management
- Profile page with user statistics
- Settings page with preferences
- Account management options

## Technology Stack

- **Framework**: Next.js 16 (App Router)
- **UI Library**: React 19
- **Language**: TypeScript 5.7
- **Styling**: Tailwind CSS 4
- **Components**: shadcn/ui
- **Animations**: Framer Motion 11
- **Icons**: Lucide React
- **Markdown**: react-markdown + highlight.js
- **Package Manager**: pnpm

## Getting Started

### Prerequisites
- Node.js 18+ (18.17.0 or higher)
- pnpm 9+

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
pnpm install

# Start development server
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start
```

The app will be available at `http://localhost:3000`

## Project Pages

| Route | Purpose |
|-------|---------|
| `/` | Landing page |
| `/auth/sign-in` | Sign in form |
| `/auth/sign-up` | Registration form |
| `/auth/forgot-password` | Password recovery |
| `/auth/verify-email` | Email verification |
| `/dashboard` | Main chat interface |
| `/dashboard/profile` | User profile |
| `/dashboard/settings` | User settings |

## Key Components

### Layout Components
- **Navbar**: Top navigation with branding and account menu
- **Sidebar**: Left sidebar with chat history and navigation

### Chat Components
- **MessageBubble**: Individual message display with markdown support
- **ChatInput**: Message input with file attachment support
- **TypingIndicator**: Animated "typing" indicator
- **EmptyState**: Welcome screen with suggestion cards

### UI Components
- **DocumentCard**: Document context display
- **ImagePreview**: Image context with expand capability
- **ErrorCard**: Error state display with actions
- **MessageLoader**: Skeleton loader for messages

### Auth Components
- **SignInForm**: Email/password sign in
- **SignUpForm**: Registration with validation
- SignIn/SignUp/ForgotPassword/VerifyEmail pages

## Hooks

### useChat
Manages chat state including messages, streaming, context files, and API interactions.

```typescript
const {
  messages,
  isLoading,
  isStreaming,
  sendMessage,
  setDocument,
  setImage,
  clearMessages,
} = useChat();
```

### useConversations
Manages conversation history and selection.

```typescript
const {
  conversations,
  currentConversationId,
  createConversation,
  deleteConversation,
  selectConversation,
} = useConversations();
```

## Utilities

### fileValidator.ts
- `validateFile()` - Validates file type and size
- `formatFileSize()` - Formats bytes to human readable
- `getFileType()` - Determines file type

### messageFormatter.ts
- `formatTime()` - Formats timestamps (e.g., "2m ago")
- `extractCodeBlocks()` - Extracts code from markdown
- `highlightCode()` - Syntax highlighting
- `generateConversationTitle()` - Creates titles from messages

## Responsive Design

- **Mobile**: Single column layout, touch-optimized
- **Tablet**: 768px+ - Sidebar becomes visible
- **Desktop**: 1024px+ - Full layout with optimal spacing
- **Large**: 1280px+ - Maximum content width with padding

## Accessibility

- Semantic HTML elements
- ARIA labels for interactive components
- Keyboard navigation support (Tab, Enter, Escape)
- Focus indicators for keyboard users
- Color contrast compliance
- Screen reader friendly text

## Performance Optimizations

- Server-side rendering (SSR) with Next.js
- Static generation where possible
- Image optimization
- Code splitting and lazy loading
- Efficient re-renders with proper memoization

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari 14+, Chrome Mobile)

## Frontend-Only Implementation

This is a **frontend-only** application designed to work with your backend API. Key points:

- No authentication logic implemented (ready for your auth service)
- No data persistence (ready for your database)
- No AI/LLM integration (ready for your model)
- Demo data used for UI/UX demonstration
- Ready for backend integration via API calls

## Future Backend Integration

To connect this frontend to your backend:

1. Update `useChat` hook to call your API endpoints
2. Implement authentication with your auth service
3. Configure API calls in utils and hooks
4. Add environment variables for API endpoints
5. Implement real-time updates (WebSocket/SSE)

## Deployment

### Vercel (Recommended)
```bash
vercel deploy
```

### Other Platforms
The app can be deployed to any Node.js hosting:
- AWS Amplify
- Netlify
- Heroku
- DigitalOcean
- Azure App Service

## License

© 2024 Intellex AI. All rights reserved.

---

Built with ❤️ using Next.js, React, and TypeScript.

### Links
https://intellex-ai-4v-b1vu2x6hf-subhasis-roy.vercel.app/
