import { PromptFeedback } from './types';

// Function to simulate API delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Mock analysis logic
export async function mockAnalyzePrompt(prompt: string): Promise<PromptFeedback> {
  // Simulate API delay
  await delay(2000);
  
  // Basic analysis logic
  const wordCount = prompt.split(/\s+/).filter(Boolean).length;
  const hasSpecificRequest = /create|design|build|implement|develop/i.test(prompt);
  const hasContext = prompt.length > 50;
  const hasFormatting = /format|style|organize/i.test(prompt);
  const hasConstraints = /don't|avoid|exclude|must not|should not/i.test(prompt);
  const hasExamples = /example|for instance|such as/i.test(prompt);

  // Calculate mock score
  let score = 5; // Base score
  
  if (wordCount > 15) score += 1;
  if (wordCount > 30) score += 1;
  if (hasSpecificRequest) score += 1;
  if (hasContext) score += 1;
  if (hasFormatting) score += 0.5;
  if (hasConstraints) score += 0.5;
  if (hasExamples) score += 1;
  
  // Clamp score between 1 and 10
  score = Math.max(1, Math.min(10, Math.round(score * 10) / 10));

  // Generate strengths
  const strengths: string[] = [];
  if (wordCount > 15) strengths.push('Good length for context');
  if (hasSpecificRequest) strengths.push('Clear request/instruction included');
  if (hasContext) strengths.push('Provides helpful context');
  if (hasFormatting) strengths.push('Specifies desired formatting');
  if (hasConstraints) strengths.push('Includes constraints/boundaries');
  if (hasExamples) strengths.push('Includes examples for clarity');
  
  // If we don't have at least 2 strengths, add some generic ones
  if (strengths.length < 2) {
    const genericStrengths = [
      'Clear objective',
      'Reasonable request',
      'Good starting point',
    ];
    
    while (strengths.length < 2 && genericStrengths.length > 0) {
      const randomStrength = genericStrengths.splice(
        Math.floor(Math.random() * genericStrengths.length), 
        1
      )[0];
      strengths.push(randomStrength);
    }
  }

  // Generate improvements
  const improvements: string[] = [];
  if (wordCount < 15) improvements.push('Add more detail to provide context');
  if (!hasSpecificRequest) improvements.push('Include a clearer instruction or request');
  if (!hasContext) improvements.push('Provide more background or context');
  if (!hasFormatting) improvements.push('Specify your preferred format or structure');
  if (!hasConstraints) improvements.push('Consider adding constraints to narrow results');
  if (!hasExamples) improvements.push('Include examples to clarify your expectations');

  // If we don't have at least 2 improvements, add some generic ones
  if (improvements.length < 2) {
    const genericImprovements = [
      'Try adding more specific requirements',
      'Consider breaking complex requests into steps',
      'Specify your audience or use case',
      'Add expected length or scope',
    ];
    
    while (improvements.length < 2 && genericImprovements.length > 0) {
      const randomImprovement = genericImprovements.splice(
        Math.floor(Math.random() * genericImprovements.length), 
        1
      )[0];
      improvements.push(randomImprovement);
    }
  }

  // Generate tags
  const allPossibleTags = [
    'creative', 'technical', 'business', 'writing', 'coding',
    'design', 'marketing', 'research', 'education', 'personal',
  ];
  
  const tags = [];
  // Add some content-related tags based on prompt
  if (/code|program|develop|api|function/i.test(prompt)) tags.push('coding');
  if (/design|layout|ui|ux|interface|website/i.test(prompt)) tags.push('design');
  if (/business|strategy|plan|company|market/i.test(prompt)) tags.push('business');
  if (/write|article|essay|content|blog/i.test(prompt)) tags.push('writing');
  
  // Add some random tags if we have less than 3
  while (tags.length < 3) {
    const randomTag = allPossibleTags[Math.floor(Math.random() * allPossibleTags.length)];
    if (!tags.includes(randomTag)) {
      tags.push(randomTag);
    }
  }

  // Generate summary
  let summary;
  if (score >= 8) {
    summary = 'Excellent prompt! Clear, detailed, and well-structured.';
  } else if (score >= 6) {
    summary = 'Good prompt with clear intent. Some minor improvements could enhance results.';
  } else if (score >= 4) {
    summary = 'Adequate prompt that could benefit from more specificity and context.';
  } else {
    summary = 'Basic prompt that needs significant improvement to get optimal results.';
  }

  return {
    score,
    strengths,
    improvements,
    tags,
    summary,
  };
}