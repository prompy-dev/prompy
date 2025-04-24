import { FeedbackData } from "@/components/feedback-display";

// Mock API function to simulate feedback generation
export async function generateFeedback(prompt: string): Promise<FeedbackData> {
  // In a real application, this would call an actual API
  return new Promise((resolve) => {
    // Simulate API call delay
    setTimeout(() => {
      // Generate random scores for demonstration
      const overallScore = Math.floor(Math.random() * 30) + 70; // 70-99
      const clarity = Math.floor(Math.random() * 40) + 60; // 60-99
      const specificity = Math.floor(Math.random() * 40) + 60; // 60-99
      const conciseness = Math.floor(Math.random() * 40) + 60; // 60-99
      
      const feedback = generateFeedbackText(prompt, overallScore);
      const improvements = generateImprovementSuggestions(prompt, clarity, specificity, conciseness);
      
      resolve({
        overallScore,
        clarity,
        specificity,
        conciseness,
        feedback,
        improvements
      });
    }, 1500); // Simulate a 1.5 second API delay
  });
}

function generateFeedbackText(prompt: string, score: number): string {
  const promptLength = prompt.length;
  const wordCount = prompt.trim().split(/\s+/).length;
  
  if (score >= 90) {
    return `Your prompt is excellent! At ${wordCount} words, it provides clear direction while maintaining conciseness. The specificity and structure make it easy for AI to understand exactly what you're looking for.`;
  } else if (score >= 80) {
    return `Your prompt is very good! With ${wordCount} words, it communicates your intent clearly. There are a few minor improvements that could make it even more effective and precise for AI interpretation.`;
  } else if (score >= 70) {
    return `Your prompt is good but has room for improvement. At ${wordCount} words, it conveys the basic idea, but could benefit from more clarity and specific instructions to guide the AI more effectively.`;
  } else {
    return `Your prompt needs significant improvement. At ${wordCount} words, it lacks clarity and specific instructions. Consider restructuring and adding more details about what you're looking for.`;
  }
}

function generateImprovementSuggestions(
  prompt: string,
  clarity: number,
  specificity: number,
  conciseness: number
): string[] {
  const suggestions: string[] = [];
  
  if (clarity < 80) {
    suggestions.push("Add more context about what you're trying to achieve.");
    suggestions.push("Use more direct and explicit language to communicate your intent.");
  }
  
  if (specificity < 80) {
    suggestions.push("Include specific examples of what you're looking for.");
    suggestions.push("Define key terms that might be ambiguous or interpreted in multiple ways.");
  }
  
  if (conciseness < 80) {
    suggestions.push("Remove redundant words and phrases to make your prompt more focused.");
    suggestions.push("Break long, complex sentences into shorter, clearer statements.");
  }
  
  if (prompt.length < 50) {
    suggestions.push("Your prompt is quite short. Consider adding more details to get better results.");
  }
  
  if (prompt.length > 500) {
    suggestions.push("Your prompt is quite long. Consider focusing on the most important aspects to improve clarity.");
  }
  
  // If we have less than 3 suggestions, add some generic ones
  if (suggestions.length < 3) {
    suggestions.push("Consider the audience or context for which you're crafting this prompt.");
    suggestions.push("Structure your prompt with clear sections: context, instructions, and expected output.");
    suggestions.push("Test your prompt with different AI models to see how they interpret it.");
  }
  
  return suggestions.slice(0, 5); // Return at most 5 suggestions
}

// Function to save prompt to history
export function savePromptToHistory(prompt: string): void {
  try {
    // Get existing history
    const historyJson = localStorage.getItem("promptHistory");
    let history: any[] = historyJson ? JSON.parse(historyJson) : [];
    
    // Add new prompt to history
    const newItem = {
      id: Date.now().toString(),
      prompt: prompt,
      timestamp: Date.now()
    };
    
    // Add to beginning of array
    history = [newItem, ...history].slice(0, 10); // Keep only 10 most recent
    
    // Save back to localStorage
    localStorage.setItem("promptHistory", JSON.stringify(history));
  } catch (e) {
    console.error("Failed to save prompt to history", e);
  }
}