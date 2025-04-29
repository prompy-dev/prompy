'use client';

import { PromptMascot } from '@/components/PromptMascot';

export function WelcomePanel() {
  return (
    <div className="h-auto flex flex-col self-center items-center justify-center py-8 px-4 space-y-4">
      <PromptMascot />
      <div>
        <h3 className="text-2xl font-bold font-walter-turncoat">
          Hi, I'm Prompy!
        </h3>
        <p className="text-md text-center font-walter-turncoat">
          Let's start prompting!
        </p>
      </div>
    </div>
  );
}
