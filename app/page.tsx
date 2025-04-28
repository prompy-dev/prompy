/**
 * @fileoverview Home page component
 * @description The main landing page of the Prompy application
 */

import { Header } from '@/components/header';
import { PromptWorkspace } from '@/components/PromptWorkspace';
import { Footer } from '@/components/footer';

/**
 * Home component
 * @description The main page component that renders the application layout
 * @returns {JSX.Element} The home page structure with header, workspace, and footer
 */
export default function Home() {
  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      <div className="flex-1 container mx-auto px-4 py-6 md:py-8 lg:py-12">
        <PromptWorkspace />
      </div>
      <Footer />
    </main>
  );
}
