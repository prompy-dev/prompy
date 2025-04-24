export interface PromptFeedback {
  score: number;
  strengths: string[];
  improvements: string[];
  tags: string[];
  summary: string;
}

export interface HistoryItem {
  id: string;
  prompt: string;
  feedback: PromptFeedback;
  timestamp: string;
}