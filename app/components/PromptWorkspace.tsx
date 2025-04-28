'use client';

import { useState } from 'react';
import { PromptPanel } from '@/components/PromptPanel';
import { FeedbackPanel } from '@/components/FeedbackPanel';
import { PromptHistory } from '@/components/PromptHistory';
import { usePromptHistory } from '@/hooks/usePromptHistory';
import { submitPrompt } from '@/lib/submitPrompt';
import { toast } from '@/hooks/use-toast';
import { ChatResponse } from '@/lib/types';

export function PromptWorkspace() {
  const [prompt, setPrompt] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [feedback, setFeedback] = useState<ChatResponse | null>(null);
  const [showFeedbackOnMobile, setShowFeedbackOnMobile] = useState(false);
  const { history, addToHistory, removeFromHistory, clearHistory } =
    usePromptHistory();

  const handleAnalyzePrompt = async () => {
    if (!prompt.trim()) {
      toast({
        title: 'Empty prompt',
        description: 'Please enter a prompt to analyze.',
        variant: 'destructive',
      });
      return;
    }

    setIsAnalyzing(true);
    setFeedback(null);
    setShowFeedbackOnMobile(true);

    try {
      const result = await submitPrompt(prompt);
      setFeedback(result);

      // Add to history
      addToHistory({
        id: Date.now().toString(),
        prompt,
        feedback: result as any, // Temporary fix until we update the history type
        timestamp: new Date().toISOString(),
      });

      toast({
        title: 'Analysis complete',
        description: 'Your prompt has been analyzed!',
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to analyze prompt. Please try again.',
        variant: 'destructive',
      });
      console.error('Error submitting prompt:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleClearPrompt = () => {
    setPrompt('');
    setFeedback(null);
    setShowFeedbackOnMobile(false);
  };

  const handleLoadFromHistory = (historyItem: any) => {
    setPrompt(historyItem.prompt);
    setFeedback(historyItem.feedback);
    setShowFeedbackOnMobile(true);
  };

  const handleBackToPrompt = () => {
    setShowFeedbackOnMobile(false);
  };

  const handleBackToFeedback = () => {
    setShowFeedbackOnMobile(true);
  };

  return (
    <div className="flex flex-col space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div
          className={`${
            isAnalyzing || showFeedbackOnMobile ? 'hidden md:block' : 'block'
          }`}
        >
          <PromptPanel
            prompt={prompt}
            onChange={setPrompt}
            onAnalyze={handleAnalyzePrompt}
            onClear={handleClearPrompt}
            isAnalyzing={isAnalyzing}
            onBack={feedback ? handleBackToFeedback : undefined}
          />
        </div>
        <div
          className={`${
            isAnalyzing || showFeedbackOnMobile ? 'block' : 'hidden md:block'
          }`}
        >
          <FeedbackPanel
            feedback={feedback}
            isLoading={isAnalyzing}
            onBack={handleBackToPrompt}
          />
        </div>
      </div>

      <PromptHistory
        history={history}
        onSelect={handleLoadFromHistory}
        onRemove={removeFromHistory}
        onClearAll={clearHistory}
      />
    </div>
  );
}
