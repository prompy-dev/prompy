/**
 * @fileoverview Application providers component
 * @description This file contains the theme provider and other application-wide providers
 */

'use client';

import { ThemeProvider } from 'next-themes';
import { useState, useEffect } from 'react';

/**
 * Providers component
 * @description Wraps the application with necessary providers (theme, etc.)
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Child components to be rendered
 * @returns {JSX.Element} The providers wrapper component
 */
export function Providers({ children }: { children: React.ReactNode }) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <>{children}</>;
  }

  return (
    <ThemeProvider attribute="class" defaultTheme="light" enableSystem>
      {children}
    </ThemeProvider>
  );
}
