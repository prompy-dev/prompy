"use client";

import { useState, useEffect } from "react";
import { 
  Clock, 
  ChevronDown,
  ChevronUp
} from "lucide-react";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";

interface PromptHistoryProps {
  onSelectPrompt: (prompt: string) => void;
}

interface HistoryItem {
  id: string;
  prompt: string;
  timestamp: number;
}

export function PromptHistory({ onSelectPrompt }: PromptHistoryProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [history, setHistory] = useState<HistoryItem[]>([]);

  useEffect(() => {
    // Load history from localStorage
    const savedHistory = localStorage.getItem("promptHistory");
    if (savedHistory) {
      try {
        setHistory(JSON.parse(savedHistory));
      } catch (e) {
        console.error("Failed to parse prompt history", e);
      }
    }
  }, []);

  const handleSelectPrompt = (prompt: string) => {
    onSelectPrompt(prompt);
    setIsOpen(false);
  };

  const formatTimestamp = (timestamp: number) => {
    const date = new Date(timestamp);
    return date.toLocaleString(undefined, {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <Collapsible
      open={isOpen}
      onOpenChange={setIsOpen}
      className="w-full"
    >
      <CollapsibleTrigger asChild>
        <Button 
          variant="ghost" 
          size="sm" 
          className="w-full flex justify-between items-center px-4 py-2 h-auto"
        >
          <div className="flex items-center">
            <Clock className="h-4 w-4 mr-2" />
            <span>Recent Prompts</span>
          </div>
          {isOpen ? (
            <ChevronUp className="h-4 w-4" />
          ) : (
            <ChevronDown className="h-4 w-4" />
          )}
        </Button>
      </CollapsibleTrigger>
      <CollapsibleContent className="overflow-hidden transition-all data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down">
        <div className="border rounded-md p-1 mt-1">
          {history.length === 0 ? (
            <div className="py-4 text-center text-sm text-muted-foreground">
              No recent prompts
            </div>
          ) : (
            <ScrollArea className="h-[200px]">
              <div className="space-y-1 p-1">
                {history.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => handleSelectPrompt(item.prompt)}
                    className="w-full text-left p-2 rounded-md hover:bg-muted text-sm transition-colors"
                  >
                    <div className="truncate">{item.prompt}</div>
                    <div className="text-xs text-muted-foreground mt-1">
                      {formatTimestamp(item.timestamp)}
                    </div>
                  </button>
                ))}
              </div>
            </ScrollArea>
          )}
        </div>
      </CollapsibleContent>
    </Collapsible>
  );
}