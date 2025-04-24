import { MessageCircle } from 'lucide-react';
import Link from 'next/link';
import Image from 'next/image';

export function Header() {
  return (
    <header className="border-b bg-white">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <Image src="/prompy.svg" alt="Prompy Logo" width={50} height={50} />
          <h1 className="text-2xl font-bold bg-gradient-to-r from-[#61dcfb] to-blue-500 bg-clip-text text-transparent">
            Prompy
          </h1>
        </Link>
        <nav className="hidden md:flex items-center gap-6">
          <Link
            href="/"
            className="text-sm font-medium hover:text-[#61dcfb] transition-colors"
          >
            Home
          </Link>
          <Link
            href="#"
            className="text-sm font-medium hover:text-[#61dcfb] transition-colors"
          >
            Examples
          </Link>
          <Link
            href="#"
            className="text-sm font-medium hover:text-[#61dcfb] transition-colors"
          >
            Guide
          </Link>
        </nav>
      </div>
    </header>
  );
}
