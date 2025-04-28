'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { PromptMascot } from '@/components/PromptMascot';
import { Badge } from '@/components/ui/badge';
import { ChatResponse } from '@/lib/types';
import Image from 'next/image';
import { Button } from './ui/button';
import { ArrowLeft } from 'lucide-react';

interface FeedbackPanelProps {
  feedback: ChatResponse | null;
  isLoading: boolean;
  onBack?: () => void;
}

export function FeedbackPanel({
  feedback,
  isLoading,
  onBack,
}: FeedbackPanelProps) {
  // Score colors
  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-500';
    if (score >= 6) return 'text-blue-500';
    if (score >= 4) return 'text-amber-500';
    return 'text-rose-500';
  };

  // Score description
  const getScoreDescription = (score: number) => {
    if (score >= 10) return 'Perfect!';
    if (score >= 8) return 'Wow!';
    if (score >= 6) return 'Nice!';
    if (score >= 4) return 'Getting there...';
    return 'Meh...';
  };

  return (
    <Card className="h-full shadow-md border-[#61dcfb]/20 transition-all relative">
      <div className="w-full flex items-center">
        {feedback && !isLoading && (
          <CardHeader className="w-full flex-row ">
            <div className="flex flex-col flex-1 justify-between">
              <CardTitle className="text-3xl font-walter-turncoat pr-0 leading-none">
                Prompy's Score
              </CardTitle>
              {onBack && (
                <Button
                  onClick={onBack}
                  className="absolute top-2 right-2 md:hidden text-[10px] px-2 py-1 h-6 bg-[#61dcfb] hover:bg-[#61dcfb]/90 text-white font-walter-turncoat"
                >
                  <ArrowLeft className="ml-1 h-3 w-3" />
                  New Prompt
                </Button>
              )}
              <div className="w-full flex items-center">
                <div className="w-full">
                  <div className="flex items-baseline justify-between">
                    <span
                      className={`text-2xl font-bold ${getScoreColor(
                        feedback.score
                      )}`}
                    >
                      {feedback.score}/10
                    </span>
                  </div>
                  <Progress
                    value={feedback.score * 10}
                    className={`h-5 bg-secondary`}
                    indicatorClassName={
                      feedback.score >= 8
                        ? 'bg-green-500'
                        : feedback.score >= 6
                        ? 'bg-blue-500'
                        : feedback.score >= 4
                        ? 'bg-amber-500'
                        : 'bg-rose-500'
                    }
                  />
                </div>
              </div>
            </div>
            <div className="flex flex-col self-center flex-1 items-center">
              <Image
                src="/prompy-basic.png"
                alt="Prompy Logo"
                width={100}
                height={100}
              />
              <span className="text-xl font-bold text-center font-walter-turncoat">
                {getScoreDescription(feedback.score)}
              </span>
            </div>
          </CardHeader>
        )}
      </div>
      <CardContent className="flex flex-col">
        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-8 px-4 space-y-4">
            <PromptMascot isAnimating />
            <p className="text-center text-muted-foreground animate-pulse pt-5">
              Let me think for a moment...
            </p>
          </div>
        ) : feedback ? (
          <div className="space-y-6">
            <div className="space-y-3">
              <h3 className="text-md font-bold font-walter-turncoat">
                What I love...
              </h3>
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
              <h3 className="text-md font-bold font-walter-turncoat">
                Where we can go with it!
              </h3>
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
              <h3 className="text-md font-bold font-walter-turncoat">Tags</h3>
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
          <div className="h-auto flex flex-col self-center items-center justify-center py-8 px-4 space-y-4 h-[200px]">
            <PromptMascot />
            <div>
              <h3 className="text-2xl font-bold font-walter-turncoat">
                Hi, I'm Prompy!
              </h3>
              <p className="text-md text-center font-walter-turncoat">
                Let's start prompting!
              </p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
