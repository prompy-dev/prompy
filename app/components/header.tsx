"use client";

import { ScanSearch } from "lucide-react";
import { ThemeToggle } from "@/components/theme-toggle";

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="flex items-center mr-4 space-x-2">
          <ScanSearch className="h-6 w-6" />
          <span className="font-bold text-lg">prompy</span>
        </div>
        
        <div className="flex flex-1 items-center justify-end">
          <nav className="flex items-center space-x-1">
            <ThemeToggle />
          </nav>
        </div>
      </div>
    </header>
  );
}