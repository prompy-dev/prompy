"use client";

import { useState, useEffect } from "react";
import { Copy, RotateCcw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";

interface PromptInputProps {
  onSubmit: (prompt: string) => void;
  isLoading: boolean;
}

export function PromptInput({ onSubmit, isLoading }: PromptInputProps) {
  const [prompt, setPrompt] = useState("");
  const [charCount, setCharCount] = useState(0);
  const [wordCount, setWordCount] = useState(0);

  useEffect(() => {
    // Update character count
    setCharCount(prompt.length);
    
    // Update word count
    const words = prompt.trim().split(/\s+/);
    setWordCount(prompt.trim() === "" ? 0 : words.length);
  }, [prompt]);

  const handleSubmit = () => {
    if (prompt.trim().length === 0) {
      toast.error("Please enter a prompt");
      return;
    }
    
    onSubmit(prompt);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(prompt);
    toast.success("Prompt copied to clipboard");
  };

  const handleClear = () => {
    setPrompt("");
  };

  return (
    <div className="flex h-full flex-col space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Your Prompt</h2>
        <div className="flex items-center space-x-2">
          <Button 
            variant="outline" 
            size="sm" 
            onClick={handleCopy}
            disabled={!prompt.length}
          >
            <Copy className="h-4 w-4 mr-2" />
            Copy
          </Button>
          <Button 
            variant="outline" 
            size="sm" 
            onClick={handleClear}
            disabled={!prompt.length}
          >
            <RotateCcw className="h-4 w-4 mr-2" />
            Clear
          </Button>
        </div>
      </div>
      
      <Textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter your prompt here..."
        className="flex-1 min-h-[200px] resize-none text-base p-4 transition-all duration-200 focus:ring-2 focus:ring-primary/50"
      />
      
      <div className="flex items-center justify-between">
        <div className="text-sm text-muted-foreground">
          {charCount} characters · {wordCount} words
        </div>
        <Button 
          onClick={handleSubmit} 
          disabled={isLoading || prompt.trim().length === 0}
          className="transition-all duration-300 relative overflow-hidden"
        >
          {isLoading ? "Analyzing..." : "Get Feedback"}
          {isLoading && (
            <span className="absolute inset-0 flex items-center justify-center bg-primary/10">
              <span className="loading loading-spinner loading-xs"></span>
            </span>
          )}
        </Button>
      </div>
    </div>
  );
}