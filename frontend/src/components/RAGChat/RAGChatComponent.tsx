import React, { useState, useRef, useEffect } from 'react';
import { UserMessage, AssistantMessage } from '../ChatMessage';
import { chatAPI } from '../chatAPI'; // Use the correct import for chat API

interface RAGChatComponentProps {
  chapterId?: number;
  onQuerySubmit?: (query: string, response: string) => void;
}

interface ChatInteraction {
  id: number;
  query: string;
  response: string;
  sources?: string[];
  timestamp: Date;
}

export const RAGChatComponent: React.FC<RAGChatComponentProps> = ({ chapterId, onQuerySubmit }) => {
  const [inputValue, setInputValue] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  // Start with an empty chat history initially
  const [chatHistory, setChatHistory] = useState<ChatInteraction[]>([]);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to history
    const userMessage: ChatInteraction = {
      id: Date.now(),
      query: inputValue,
      response: '', // Will be filled when we get the response
      timestamp: new Date(),
    };

    setChatHistory(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the actual backend API to process the query
      const response = await chatAPI.sendMessage(inputValue);

      const assistantMessage: ChatInteraction = {
        id: Date.now() + 1,
        query: inputValue,
        response: response.response,
        sources: response.sources || [],
        timestamp: new Date(),
      };

      setChatHistory(prev => {
        const updatedHistory = [...prev];
        // Update the last message with the response
        updatedHistory[updatedHistory.length - 1] = assistantMessage;
        return updatedHistory;
      });

      // Notify parent component if callback is provided
      if (onQuerySubmit) {
        onQuerySubmit(inputValue, response.response);
      }
    } catch (error: any) {
      console.error('Error getting AI response:', error);
      const errorMessage: ChatInteraction = {
        id: Date.now() + 1,
        query: inputValue,
        response: `Sorry, I'm having trouble accessing the textbook content right now. Error: ${error.message || 'Unknown error'}. Please try again later. This AI assistant only responds based on information found in the Physical AI textbook.`,
        timestamp: new Date(),
      };
      setChatHistory(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Scroll to bottom when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  return (
    <div className="flex flex-col h-full border border-gray-200 rounded-xl shadow-sm bg-white">
      <div className="p-4 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-t-xl">
        <h3 className="text-lg font-semibold text-gray-900 flex items-center">
          <span className="mr-2">🤖</span> AI Textbook Assistant
        </h3>
        <p className="text-sm text-gray-600 mt-1">
          Ask questions about the textbook content. I only respond based on the book content with proper citations.
        </p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 bg-gray-50 max-h-[400px]">
        {chatHistory.length === 0 ? (
          <div className="text-center text-gray-500 py-8">
            <div className="mb-4">
              <div className="inline-block p-3 bg-blue-100 rounded-full">
                <span className="text-2xl">📚</span>
              </div>
            </div>
            <p>Ask your first question about the Physical AI textbook!</p>
            <p className="text-sm mt-2 text-gray-400">Try asking about specific topics from the curriculum</p>
          </div>
        ) : (
          <div className="space-y-4">
            {chatHistory.map((interaction) => (
              <div key={interaction.id}>
                <UserMessage text={interaction.query} timestamp={interaction.timestamp} />
                {interaction.response && (
                  <AssistantMessage
                    text={interaction.response}
                    timestamp={interaction.timestamp}
                    sources={interaction.sources ? interaction.sources.map(source => ({
                      title: source,
                      url: '', // We might need to enhance this with actual URLs if available
                    })) : undefined}
                  />
                )}
              </div>
            ))}
            {isLoading && (
              <div className="flex items-center space-x-2 text-blue-600 animate-pulse">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                <span>Analyzing textbook content...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200 bg-white rounded-b-xl">
        <div className="flex">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask a question about the textbook content..."
            className="flex-1 border border-gray-300 rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded-r-lg hover:bg-blue-700 disabled:opacity-50 transition"
            disabled={isLoading || !inputValue.trim()}
          >
            Send
          </button>
        </div>
        <p className="text-xs text-gray-600 mt-2">
          AI assistant responds only from textbook content • Citations provided for all answers
        </p>
      </form>
    </div>
  );
};