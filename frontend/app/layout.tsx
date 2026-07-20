import { Analytics } from '@vercel/analytics/next'
import type { Metadata, Viewport } from 'next'
import { Geist, Geist_Mono } from 'next/font/google'
import './globals.css'

const geistSans = Geist({ subsets: ['latin'] })
const geistMono = Geist_Mono({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Intellex AI - Premium AI Platform',
  description:
    'Experience the future of artificial intelligence with Intellex - a premium platform for intelligent conversations, document analysis, and image processing.',
  keywords: ['AI', 'Chat', 'Intelligence', 'Premium', 'Analytics'],
  authors: [{ name: 'Intellex AI' }],
  openGraph: {
    title: 'Intellex AI - Premium AI Platform',
    description: 'Experience the future of artificial intelligence',
    type: 'website',
  },
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
  colorScheme: 'dark',
  themeColor: '#d4af37',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className="bg-background">
      <body className={`${geistSans.className} antialiased bg-background text-text-primary`}>
        {children}
        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}
