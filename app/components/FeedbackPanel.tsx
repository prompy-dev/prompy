'use client';

import { Card } from '@/components/ui/card';
import { PromptMascot } from '@/components/PromptMascot';
import { ChatResponse } from '@/lib/types';
import { WelcomePanel } from './WelcomePanel';
import { ScorePanelHeader } from './ScorePanelHeader';
import { ScorePanelBody } from './ScorePanelBody';

interface FeedbackPanelProps {
  feedback: ChatResponse | null;
  isLoading: boolean;
  onBack?: () => void;
}

export function FeedbackPanel({
  feedback,
  isLoading,
  onBack,
}: FeedbackPanelProps) {
  return (
    <Card className="h-full shadow-md border-[#61dcfb]/20 transition-all relative">
      <div className="w-full flex items-center">
        {feedback && !isLoading && (
          <ScorePanelHeader feedback={feedback} onBack={onBack} />
        )}
      </div>
      {isLoading ? (
        <div className="flex flex-col items-center justify-center py-8 px-4 space-y-4">
          <PromptMascot isAnimating />
          <p className="text-center text-muted-foreground animate-pulse pt-5">
            Let me think for a moment...
          </p>
        </div>
      ) : feedback ? (
        <ScorePanelBody feedback={feedback} />
      ) : (
        <WelcomePanel />
      )}
    </Card>
  );
}
