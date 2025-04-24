'use client';

import { useState } from 'react';
import { PromptPanel } from '@/components/PromptPanel';
import { FeedbackPanel } from '@/components/FeedbackPanel';
import { PromptHistory } from '@/components/PromptHistory';
import { usePromptHistory } from '@/hooks/usePromptHistory';
import { mockAnalyzePrompt } from '@/lib/mockApi';
import { toast } from '@/hooks/use-toast';
import { PromptFeedback } from '@/lib/types';

export function PromptWorkspace() {
  const [prompt, setPrompt] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [feedback, setFeedback] = useState<PromptFeedback | null>(null);
  const { history, addToHistory, removeFromHistory, clearHistory } = usePromptHistory();

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

    try {
      // Simulate API call with our mock
      const result = await mockAnalyzePrompt(prompt);
      setFeedback(result);
      
      // Add to history
      addToHistory({
        id: Date.now().toString(),
        prompt,
        feedback: result,
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
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleClearPrompt = () => {
    setPrompt('');
    setFeedback(null);
  };

  const handleLoadFromHistory = (historyItem: any) => {
    setPrompt(historyItem.prompt);
    setFeedback(historyItem.feedback);
  };

  return (
    <div className="flex flex-col space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <PromptPanel
          prompt={prompt}
          onChange={setPrompt}
          onAnalyze={handleAnalyzePrompt}
          onClear={handleClearPrompt}
          isAnalyzing={isAnalyzing}
        />
        <FeedbackPanel feedback={feedback} isLoading={isAnalyzing} />
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