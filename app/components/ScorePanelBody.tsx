'use client';

import { CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ChatResponse } from '@/lib/types';

interface ScorePanelBodyProps {
  feedback: ChatResponse;
}

export function ScorePanelBody({ feedback }: ScorePanelBodyProps) {
  return (
    <CardContent className="flex flex-col">
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
    </CardContent>
  );
}
