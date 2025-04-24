'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { PromptMascot } from '@/components/PromptMascot';
import { Badge } from '@/components/ui/badge';
import { PromptFeedback } from '@/lib/types';

interface FeedbackPanelProps {
  feedback: PromptFeedback | null;
  isLoading: boolean;
}

export function FeedbackPanel({ feedback, isLoading }: FeedbackPanelProps) {
  // Score colors
  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-500';
    if (score >= 6) return 'text-blue-500';
    if (score >= 4) return 'text-amber-500';
    return 'text-rose-500';
  };

  // Score description
  const getScoreDescription = (score: number) => {
    if (score >= 8) return 'Excellent';
    if (score >= 6) return 'Good';
    if (score >= 4) return 'Adequate';
    return 'Needs Improvement';
  };

  return (
    <Card className="h-full shadow-md border-[#61dcfb]/20 transition-all hover:shadow-lg relative overflow-hidden">
      <CardHeader>
        {(feedback && !isLoading) && (<CardTitle className="text-lg flex items-center gap-2">
          <span className="text-[#61dcfb]">💡</span> Feedback
        </CardTitle>)}
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-8 px-4 space-y-4">
            <PromptMascot isAnimating />
            <p className="text-center text-muted-foreground animate-pulse">
              Prompy is thinking...
            </p>
          </div>
        ) : feedback ? (
          <div className="space-y-6">
            <div className="space-y-2">
              <div className="flex items-baseline justify-between">
                <h3 className="text-sm font-medium text-muted-foreground">
                  Score
                </h3>
                <div className="flex items-baseline gap-2">
                  <span
                    className={`text-2xl font-bold ${getScoreColor(
                      feedback.score
                    )}`}
                  >
                    {feedback.score}/10
                  </span>
                  <span className="text-sm text-muted-foreground">
                    ({getScoreDescription(feedback.score)})
                  </span>
                </div>
              </div>
              <Progress
                value={feedback.score * 10}
                className={`h-2 ${
                  feedback.score >= 8
                    ? 'bg-green-500'
                    : feedback.score >= 6
                    ? 'bg-blue-500'
                    : feedback.score >= 4
                    ? 'bg-amber-500'
                    : 'bg-rose-500'
                }`}
              />
            </div>

            <div className="space-y-3">
              <h3 className="text-sm font-medium">Strengths</h3>
              <ul className="space-y-2">
                {feedback.strengths.map((strength, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <span className="text-green-500 mt-0.5">✓</span>
                    <span>{strength}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="space-y-3">
              <h3 className="text-sm font-medium">Areas for Improvement</h3>
              <ul className="space-y-2">
                {feedback.improvements.map((improvement, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <span className="text-amber-500 mt-0.5">!</span>
                    <span>{improvement}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="space-y-3">
              <h3 className="text-sm font-medium">Tags</h3>
              <div className="flex flex-wrap gap-2">
                {feedback.tags.map((tag, i) => (
                  <Badge
                    key={i}
                    variant="secondary"
                    className="bg-[#61dcfb]/10 hover:bg-[#61dcfb]/20 text-[#61dcfb]"
                  >
                    {tag}
                  </Badge>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-8 px-4 space-y-4 h-[200px]">
            <PromptMascot />
            <div>
              <p className="text-center">Hi, I'm Prompy!</p>
              <p className="text-center">Let's start prompting!</p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
