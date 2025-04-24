import { Header } from '@/components/Header';
import { PromptWorkspace } from '@/components/PromptWorkspace';
import { Footer } from '@/components/Footer';

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