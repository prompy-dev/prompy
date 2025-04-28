import './globals.css';
import type { Metadata } from 'next';
import { Inter, Walter_Turncoat } from 'next/font/google';
import { Providers } from './providers';
import { Toaster } from '@/components/ui/toaster';

const inter = Inter({ subsets: ['latin'] });
const walterTurncoat = Walter_Turncoat({
  weight: '400',
  subsets: ['latin'],
  variable: '--font-walter-turncoat',
});

export const metadata: Metadata = {
  title: 'Prompy - AI Prompt Writing Coach',
  description:
    'Get feedback and improve your AI prompts with Prompy, your personal prompt writing coach',
};

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
