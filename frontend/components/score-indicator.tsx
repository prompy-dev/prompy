"use client";

import { useState, useEffect } from "react";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";

interface ScoreIndicatorProps {
  score: number;
  primary?: boolean;
}

export function ScoreIndicator({ score, primary = false }: ScoreIndicatorProps) {
  const [progress, setProgress] = useState(0);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setProgress(score);
    }, 100);
    
    return () => clearTimeout(timer);
  }, [score]);
  
  const getScoreColor = (score: number) => {
    if (score >= 90) return "text-green-500 dark:text-green-400";
    if (score >= 70) return "text-emerald-500 dark:text-emerald-400";
    if (score >= 50) return "text-amber-500 dark:text-amber-400";
    if (score >= 30) return "text-orange-500 dark:text-orange-400";
    return "text-red-500 dark:text-red-400";
  };
  
  const getProgressColor = (score: number) => {
    if (score >= 90) return "bg-green-500 dark:bg-green-400";
    if (score >= 70) return "bg-emerald-500 dark:bg-emerald-400";
    if (score >= 50) return "bg-amber-500 dark:bg-amber-400";
    if (score >= 30) return "bg-orange-500 dark:bg-orange-400";
    return "bg-red-500 dark:bg-red-400";
  };
  
  return (
    <div className="space-y-2">
      <div className="flex items-baseline justify-between">
        <span className={cn(
          getScoreColor(score),
          primary ? "text-3xl font-bold" : "text-xl font-semibold"
        )}>
          {score}
        </span>
        <span className="text-xs text-muted-foreground">out of 100</span>
      </div>
      
      <Progress 
        value={progress} 
        className="h-2 transition-all duration-500"
        indicatorClassName={getProgressColor(score)}
      />
      
      <div className="flex justify-between text-xs text-muted-foreground">
        <span>Poor</span>
        <span>Excellent</span>
      </div>
    </div>
  );
}