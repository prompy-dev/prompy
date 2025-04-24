'use client';

import { useState } from 'react';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { Button } from '@/components/ui/button';
import { ChevronDown, ChevronUp, Trash } from 'lucide-react';
import { PromptItem } from '@/components/PromptItem';
import { HistoryItem } from '@/lib/types';
import { useToast } from '@/hooks/use-toast';
import { Alert, AlertDescription } from '@/components/ui/alert';

interface PromptHistoryProps {
  history: HistoryItem[];
  onSelect: (item: HistoryItem) => void;
  onRemove: (id: string) => void;
  onClearAll: () => void;
}

export function PromptHistory({ 
  history, 
  onSelect, 
  onRemove, 
  onClearAll 
}: PromptHistoryProps) {
  const [isOpen, setIsOpen] = useState(false);
  const { toast } = useToast();

  const handleClearAll = () => {
    if (history.length === 0) {
      toast({
        title: 'History is already empty',
        description: 'There are no items to clear.',
      });
      return;
    }
    
    onClearAll();
    toast({
      title: 'History cleared',
      description: 'All prompt history has been cleared.',
    });
  };

  return (
    <Collapsible open={isOpen} onOpenChange={setIsOpen} className="w-full">
      <Card className="shadow-sm border-[#61dcfb]/10">
        <CardHeader className="py-3 px-4">
          <div className="flex items-center justify-between">
            <CardTitle className="text-lg flex items-center gap-2">
              <span className="text-[#61dcfb]">🕒</span> Prompt History
            </CardTitle>
            <CollapsibleTrigger asChild>
              <Button variant="ghost" size="sm">
                {isOpen ? (
                  <ChevronUp className="h-4 w-4" />
                ) : (
                  <ChevronDown className="h-4 w-4" />
                )}
              </Button>
            </CollapsibleTrigger>
          </div>
        </CardHeader>
        
        <CollapsibleContent>
          <CardContent className="px-4 pt-0 pb-3">
            {history.length > 0 ? (
              <div className="grid grid-cols-1 gap-3 max-h-[400px] overflow-y-auto pr-2">
                {history.map((item) => (
                  <PromptItem 
                    key={item.id}
                    item={item}
                    onSelect={() => onSelect(item)}
                    onRemove={() => onRemove(item.id)}
                  />
                ))}
              </div>
            ) : (
              <Alert variant="default" className="bg-muted/50 border-muted">
                <AlertDescription className="text-sm text-muted-foreground text-center py-2">
                  Your prompt history will appear here after you analyze prompts.
                </AlertDescription>
              </Alert>
            )}
          </CardContent>
          
          {history.length > 0 && (
            <CardFooter className="px-4 pt-0 pb-3 flex justify-end">
              <Button 
                variant="outline" 
                size="sm" 
                className="text-muted-foreground hover:text-destructive hover:border-destructive"
                onClick={handleClearAll}
              >
                <Trash className="mr-2 h-4 w-4" />
                Clear All History
              </Button>
            </CardFooter>
          )}
        </CollapsibleContent>
      </Card>
    </Collapsible>
  );
}