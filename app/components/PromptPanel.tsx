'use client';

import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { RefreshCw, SendHorizonal, Trash2 } from 'lucide-react';

interface PromptPanelProps {
  prompt: string;
  onChange: (value: string) => void;
  onAnalyze: () => void;
  onClear: () => void;
  isAnalyzing: boolean;
}

export function PromptPanel({ 
  prompt, 
  onChange, 
  onAnalyze, 
  onClear, 
  isAnalyzing 
}: PromptPanelProps) {
  return (
    <Card className="h-full shadow-md border-[#61dcfb]/20 transition-all hover:shadow-lg">
      <CardHeader>
        <CardTitle className="text-lg flex items-center gap-2">
          <span className="text-[#61dcfb]">✏️</span> Your Prompt
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Textarea
          placeholder="Enter your prompt here... (e.g., 'Create a landing page for a fitness app')"
          className="min-h-[200px] resize-none focus-visible:ring-[#61dcfb]/50"
          value={prompt}
          onChange={(e) => onChange(e.target.value)}
          disabled={isAnalyzing}
        />
      </CardContent>
      <CardFooter className="flex justify-between gap-2">
        <Button 
          variant="outline" 
          size="sm" 
          onClick={onClear}
          disabled={isAnalyzing || !prompt}
        >
          <Trash2 className="mr-2 h-4 w-4" />
          Clear
        </Button>
        <Button 
          onClick={onAnalyze} 
          disabled={isAnalyzing || !prompt.trim()}
          size="sm"
          className="bg-[#61dcfb] hover:bg-[#61dcfb]/90 text-white"
        >
          {isAnalyzing ? (
            <>
              <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
              Analyzing...
            </>
          ) : (
            <>
              <SendHorizonal className="mr-2 h-4 w-4" />
              Analyze Prompt
            </>
          )}
        </Button>
      </CardFooter>
    </Card>
  );
}