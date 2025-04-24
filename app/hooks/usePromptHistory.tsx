'use client';

import { useState, useEffect } from 'react';
import { HistoryItem } from '@/lib/types';

export function usePromptHistory() {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  
  // Load history from localStorage on mount
  useEffect(() => {
    const savedHistory = localStorage.getItem('prompy-history');
    if (savedHistory) {
      try {
        setHistory(JSON.parse(savedHistory));
      } catch (error) {
        console.error('Failed to parse history from localStorage:', error);
        // If parsing fails, reset localStorage
        localStorage.setItem('prompy-history', JSON.stringify([]));
      }
    }
  }, []);
  
  // Save history to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('prompy-history', JSON.stringify(history));
  }, [history]);
  
  // Add a new item to history
  const addToHistory = (item: HistoryItem) => {
    setHistory(prev => [item, ...prev].slice(0, 50)); // Limit to 50 items
  };
  
  // Remove an item from history
  const removeFromHistory = (id: string) => {
    setHistory(prev => prev.filter(item => item.id !== id));
  };
  
  // Clear all history
  const clearHistory = () => {
    setHistory([]);
  };
  
  return {
    history,
    addToHistory,
    removeFromHistory,
    clearHistory,
  };
}