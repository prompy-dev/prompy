'use client';

import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Trash2, ArrowUpRight } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { HistoryItem } from '@/lib/types';
import { formatDistanceToNow } from 'date-fns';

interface PromptItemProps {
  item: HistoryItem;
  onSelect: () => void;
  onRemove: () => void;
}

export function PromptItem({ item, onSelect, onRemove }: PromptItemProps) {
  // Format the timestamp
  const formattedTime = formatDistanceToNow(new Date(item.timestamp), { addSuffix: true });
  
  // Truncate prompt if too long
  const truncateText = (text: string, maxLength = 100) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  // Get appropriate color for the score badge
  const getScoreBadgeColor = (score: number) => {
    if (score >= 8) return 'bg-green-100 text-green-800 hover:bg-green-200';
    if (score >= 6) return 'bg-blue-100 text-blue-800 hover:bg-blue-200';
    if (score >= 4) return 'bg-amber-100 text-amber-800 hover:bg-amber-200';
    return 'bg-rose-100 text-rose-800 hover:bg-rose-200';
  };

  return (
    <Card className="p-3 border-muted/50 hover:border-[#61dcfb]/30 transition-all cursor-pointer" onClick={onSelect}>
      <div className="flex justify-between items-start gap-2">
        <div className="flex-1 space-y-1.5">
          <div className="flex items-center justify-between">
            <Badge className={getScoreBadgeColor(item.feedback.score)}>
              Score: {item.feedback.score}/10
            </Badge>
            <span className="text-xs text-muted-foreground">{formattedTime}</span>
          </div>
          <p className="text-sm line-clamp-2">{truncateText(item.prompt)}</p>
          
          <div className="flex gap-1 flex-wrap">
            {item.feedback.tags.slice(0, 3).map((tag, i) => (
              <Badge key={i} variant="outline" className="text-xs px-1 py-0">
                {tag}
              </Badge>
            ))}
            {item.feedback.tags.length > 3 && (
              <Badge variant="outline" className="text-xs px-1 py-0">
                +{item.feedback.tags.length - 3}
              </Badge>
            )}
          </div>
        </div>
        
        <div className="flex flex-col gap-1">
          <Button
            variant="ghost" 
            size="icon" 
            className="h-6 w-6 text-muted-foreground hover:text-primary"
            onClick={(e) => {
              e.stopPropagation();
              onSelect();
            }}
          >
            <ArrowUpRight className="h-3.5 w-3.5" />
            <span className="sr-only">Open</span>
          </Button>
          
          <Button
            variant="ghost" 
            size="icon" 
            className="h-6 w-6 text-muted-foreground hover:text-destructive"
            onClick={(e) => {
              e.stopPropagation();
              onRemove();
            }}
          >
            <Trash2 className="h-3.5 w-3.5" />
            <span className="sr-only">Delete</span>
          </Button>
        </div>
      </div>
    </Card>
  );
}