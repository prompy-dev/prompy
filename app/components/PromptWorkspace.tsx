/**
 * @fileoverview PromptWorkspace component
 * @description Main workspace component for prompt analysis and feedback
 */

'use client';

import { useState } from 'react';
import { PromptPanel } from '@/components/PromptPanel';
import { FeedbackPanel } from '@/components/FeedbackPanel';
import { PromptHistory } from '@/components/PromptHistory';
import { usePromptHistory } from '@/hooks/usePromptHistory';
import { submitPrompt } from '@/lib/submitPrompt';
import { toast } from '@/hooks/use-toast';
import { ChatResponse } from '@/lib/types';

/**
 * PromptWorkspace component
 * @description Main component that handles prompt analysis, feedback display, and history management
 * @returns {JSX.Element} The workspace layout with prompt input, feedback, and history sections
 */
export function PromptWorkspace() {
  const [prompt, setPrompt] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [feedback, setFeedback] = useState<ChatResponse | null>(null);
  const [showFeedbackOnMobile, setShowFeedbackOnMobile] = useState(false);
  const { history, addToHistory, removeFromHistory, clearHistory } =
    usePromptHistory();

  /**
   * Handles the prompt analysis process
   * @async
   * @returns {Promise<void>}
   */
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

  /**
   * Clears the current prompt and feedback
   */
  const handleClearPrompt = () => {
    setPrompt('');
    setFeedback(null);
    setShowFeedbackOnMobile(false);
  };

  /**
   * Loads a prompt from history
   * @param {Object} historyItem - The history item to load
   */
  const handleLoadFromHistory = (historyItem: any) => {
    setPrompt(historyItem.prompt);
    setFeedback(historyItem.feedback);
    setShowFeedbackOnMobile(true);
  };

  /**
   * Returns to the prompt input view
   */
  const handleBackToPrompt = () => {
    setShowFeedbackOnMobile(false);
  };

  /**
   * Returns to the feedback view
   */
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
