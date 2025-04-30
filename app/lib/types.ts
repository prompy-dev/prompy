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
  feedback: ChatResponse;
  timestamp: string;
}

export interface PromptResponse {
  success: boolean;
  feedback: ChatResponse;
}

export interface ChatResponse {
  score: number;
  strengths: string[];
  improvements: string[];
  tags: string[];
}

export interface PromptAnalysis {
  response: PromptResponse;
  error?: string;
}
