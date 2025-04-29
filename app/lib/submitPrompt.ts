import { ChatResponse } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

export async function submitPrompt(prompt: string): Promise<ChatResponse> {
  try {
    const response = await fetch(`${API_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    const chatResponse = JSON.parse(data.chat_response);

    // Validate the response structure
    if (
      !chatResponse.score ||
      !Array.isArray(chatResponse.strengths) ||
      !Array.isArray(chatResponse.improvements) ||
      !Array.isArray(chatResponse.tags)
    ) {
      throw new Error(
        'Invalid response format: missing required fields or incorrect types'
      );
    }

    return chatResponse as ChatResponse;
  } catch (error) {
    console.error('Error sending prompt to OpenAI:', error);
    throw error;
  }
}
