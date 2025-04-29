'use client';

import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Trash2, ArrowRight } from 'lucide-react';

interface PromptPanelProps {
  prompt: string;
  onChange: (value: string) => void;
  onAnalyze: () => void;
  onClear: () => void;
  isAnalyzing: boolean;
  onBack?: () => void;
}

export function PromptPanel({
  prompt,
  onChange,
  onAnalyze,
  onClear,
  isAnalyzing,
  onBack,
}: PromptPanelProps) {
  // Character count to prevent exceeding 1000 characters
  const charCount = prompt.length;
  const isWarning = charCount > 800 && charCount <= 1000;
  const isError = charCount > 1000;

  return (
    <Card className="h-fit shadow-md border-[#61dcfb]/20 transition-all">
      <CardHeader className="relative">
        <CardTitle className="text-3xl flex items-center gap-2 font-walter-turncoat">
          Your Prompt
        </CardTitle>
        {onBack && (
          <Button
            onClick={onBack}
            className="absolute top-1 right-2 md:hidden text-[10px] px-2 py-1 h-6 bg-[#61dcfb] hover:bg-[#61dcfb]/90 text-white font-walter-turncoat"
          >
            Feedback
            <ArrowRight className="ml-1 h-3 w-3" />
          </Button>
        )}
      </CardHeader>
      <CardContent>
        <Textarea
          placeholder="Enter your prompt here... (e.g., 'Create a landing page for a fitness app')"
          className="min-h-[200px] resize-none focus-visible:ring-[#61dcfb]/50"
          value={prompt}
          onChange={(e) => onChange(e.target.value)}
          disabled={isAnalyzing}
        />
        <div
          className={`mt-2 text-sm ${
            isWarning
              ? 'text-orange-500'
              : isError
              ? 'text-red-500'
              : 'text-gray-500'
          }`}
        >
          {charCount > 800 && (
            <span>
              {charCount}/1000 characters
              {isError && ' - Maximum character limit exceeded'}
            </span>
          )}
        </div>
      </CardContent>
      <CardFooter className="flex justify-between gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={onClear}
          disabled={isAnalyzing || !prompt}
        >
          <Trash2 className="mr-2 h-4 w-4" />
          <span className="text-lg font-walter-turncoat">Start over</span>
        </Button>
        <Button
          onClick={onAnalyze}
          disabled={isAnalyzing || !prompt.trim() || isError}
          size="sm"
          className="bg-[#61dcfb] hover:bg-[#61dcfb]/90 text-white"
        >
          {isAnalyzing ? (
            <>Thinking...</>
          ) : (
            <span className="text-lg font-walter-turncoat">Coach me!</span>
          )}
        </Button>
      </CardFooter>
    </Card>
  );
}
