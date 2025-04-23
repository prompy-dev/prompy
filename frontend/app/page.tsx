"use client";

import { useState } from "react";
import { Header } from "@/components/header";
import { Footer } from "@/components/footer";
import { PromptInput } from "@/components/prompt-input";
import { FeedbackDisplay, FeedbackData } from "@/components/feedback-display";
import { PromptHistory } from "@/components/prompt-history";
import { Toaster } from "@/components/ui/sonner";
import { generateFeedback, savePromptToHistory } from "@/lib/mock-data";
import { motion } from "framer-motion";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [feedback, setFeedback] = useState<FeedbackData | null>(null);

  const handlePromptSubmit = async (inputPrompt: string) => {
    setIsLoading(true);
    setPrompt(inputPrompt);
    
    try {
      // Save prompt to history
      savePromptToHistory(inputPrompt);
      
      // Get feedback
      const result = await generateFeedback(inputPrompt);
      setFeedback(result);
    } catch (error) {
      console.error("Error generating feedback:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectFromHistory = (historyPrompt: string) => {
    setPrompt(historyPrompt);
  };

  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      
      <motion.main 
        className="flex-1 container py-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="space-y-6">
          <h1 className="text-3xl font-bold tracking-tight lg:text-4xl">
            Improve your prompts with AI feedback
          </h1>
          
          <div className="lg:hidden">
            <PromptHistory onSelectPrompt={handleSelectFromHistory} />
          </div>
          
          <div className="grid gap-6 lg:grid-cols-2 lg:gap-10">
            <div className="space-y-4">
              <div className="hidden lg:block">
                <PromptHistory onSelectPrompt={handleSelectFromHistory} />
              </div>
              
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2, duration: 0.4 }}
                className="border rounded-lg shadow-sm p-4 lg:p-6 bg-card"
              >
                <PromptInput 
                  onSubmit={handlePromptSubmit} 
                  isLoading={isLoading} 
                />
              </motion.div>
            </div>
            
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3, duration: 0.4 }}
              className="border rounded-lg shadow-sm p-4 lg:p-6 bg-card"
            >
              <FeedbackDisplay 
                feedback={feedback} 
                isLoading={isLoading} 
              />
            </motion.div>
          </div>
        </div>
      </motion.main>
      
      <Footer />
      <Toaster />
    </div>
  );
}