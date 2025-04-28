/**
 * @fileoverview Root layout component for the Prompy application
 * @description This file contains the root layout configuration including fonts, metadata, and providers
 */

import './globals.css';
import type { Metadata } from 'next';
import { Inter, Walter_Turncoat } from 'next/font/google';
import { Providers } from './providers';
import { Toaster } from '@/components/ui/toaster';

/**
 * Inter font configuration for the application
 */
const inter = Inter({ subsets: ['latin'] });

/**
 * Walter Turncoat font configuration for decorative elements
 */
const walterTurncoat = Walter_Turncoat({
  weight: '400',
  subsets: ['latin'],
  variable: '--font-walter-turncoat',
});

/**
 * Application metadata configuration
 */
export const metadata: Metadata = {
  title: 'Prompy - AI Prompt Writing Coach',
  description:
    'Get feedback and improve your AI prompts with Prompy, your personal prompt writing coach',
};

/**
 * RootLayout component
 * @description The root layout component that wraps the entire application
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Child components to be rendered
 * @returns {JSX.Element} The root layout structure
 */
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${inter.className} ${walterTurncoat.variable}`}
    >
      <body>
        <Providers>
          {children}
          <Toaster />
        </Providers>
      </body>
    </html>
  );
}
