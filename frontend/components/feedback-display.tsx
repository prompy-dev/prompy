"use client";

import { Copy } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ScoreIndicator } from "@/components/score-indicator";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

interface FeedbackDisplayProps {
  feedback: FeedbackData | null;
  isLoading: boolean;
}

export interface FeedbackData {
  overallScore: number;
  clarity: number;
  specificity: number;
  conciseness: number;
  feedback: string;
  improvements: string[];
}

export function FeedbackDisplay({ feedback, isLoading }: FeedbackDisplayProps) {
  const handleCopyFeedback = () => {
    if (!feedback) return;
    
    navigator.clipboard.writeText(feedback.feedback);
    toast.success("Feedback copied to clipboard");
  };

  return (
    <div className="flex h-full flex-col space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">AI Feedback</h2>
        {feedback && (
          <Button variant="outline" size="sm" onClick={handleCopyFeedback}>
            <Copy className="h-4 w-4 mr-2" />
            Copy
          </Button>
        )}
      </div>

      <div className={cn(
        "flex-1 transition-opacity duration-300",
        isLoading ? "opacity-50" : "opacity-100"
      )}>
        {feedback ? (
          <div className="space-y-6">
            <div className="grid gap-4 md:grid-cols-2">
              <Card>
                <CardContent className="pt-6">
                  <div className="space-y-2">
                    <h3 className="font-medium">Overall Score</h3>
                    <ScoreIndicator score={feedback.overallScore} primary />
                  </div>
                </CardContent>
              </Card>
              
              <div className="grid grid-cols-3 gap-2">
                <Card>
                  <CardContent className="p-3">
                    <div className="space-y-2">
                      <h3 className="text-sm font-medium">Clarity</h3>
                      <ScoreIndicator score={feedback.clarity} />
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="p-3">
                    <div className="space-y-2">
                      <h3 className="text-sm font-medium">Specificity</h3>
                      <ScoreIndicator score={feedback.specificity} />
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="p-3">
                    <div className="space-y-2">
                      <h3 className="text-sm font-medium">Conciseness</h3>
                      <ScoreIndicator score={feedback.conciseness} />
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
            
            <div className="space-y-4">
              <Card>
                <CardContent className="pt-6">
                  <div className="space-y-2">
                    <h3 className="font-medium">Feedback</h3>
                    <p className="text-muted-foreground">{feedback.feedback}</p>
                  </div>
                </CardContent>
              </Card>
              
              <Card>
                <CardContent className="pt-6">
                  <div className="space-y-2">
                    <h3 className="font-medium">Suggested Improvements</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      {feedback.improvements.map((improvement, i) => (
                        <li key={i} className="text-sm text-muted-foreground">{improvement}</li>
                      ))}
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-center p-6 border border-dashed rounded-lg space-y-4">
            <div className="text-4xl">✨</div>
            <h3 className="text-xl font-medium">No feedback yet</h3>
            <p className="text-muted-foreground max-w-md">
              Enter your prompt on the left and click "Get Feedback" to receive AI-powered analysis and suggestions.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}