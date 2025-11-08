/**
 * ChatInterface Component
 * Main chat container with state management and API integration
 */

'use client';

import { useState, useCallback, useEffect } from 'react';
import MessageList from './MessageList';
import ChatInput from './ChatInput';
import ErrorMessage from './ErrorMessage';
import { sendMessage } from '@/lib/api';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  agentType?: 'billing' | 'technical' | 'policy';
}

export default function ChatInterface() {
  // State management
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [streamingMessage, setStreamingMessage] = useState('');
  const [streamingAgentType, setStreamingAgentType] = useState<
    'billing' | 'technical' | 'policy' | undefined
  >(undefined);
  const [lastUserMessage, setLastUserMessage] = useState('');

  // Generate session ID on mount
  useEffect(() => {
    // Use crypto.randomUUID if available, otherwise fallback
    if (typeof window !== 'undefined' && window.crypto?.randomUUID) {
      setSessionId(window.crypto.randomUUID());
    } else {
      // Simple fallback UUID generation
      const uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
        const r = (Math.random() * 16) | 0;
        const v = c === 'x' ? r : (r & 0x3) | 0x8;
        return v.toString(16);
      });
      setSessionId(uuid);
    }
  }, []);

  const handleSendMessage = useCallback(
    async (messageText: string) => {
      if (!messageText.trim() || isLoading) return;

      // Clear any previous errors
      setError(null);
      setLastUserMessage(messageText);

      // Add user message to conversation
      const userMessage: Message = {
        role: 'user',
        content: messageText,
      };
      setMessages((prev) => [...prev, userMessage]);

      // Start loading
      setIsLoading(true);
      setStreamingMessage('');
      setStreamingAgentType(undefined);

      // Use a variable to accumulate the complete message
      let accumulatedMessage = '';

      try {
        // Send message and handle streaming response
        await sendMessage(messageText, sessionId, {
          onStart: (newSessionId) => {
            if (!sessionId) {
              setSessionId(newSessionId);
            }
          },

          onAgent: (agentType) => {
            setStreamingAgentType(agentType);
          },

          onToken: (token) => {
            accumulatedMessage += token;
            setStreamingMessage(accumulatedMessage);
          },

          onComplete: (completedSessionId, agentType) => {
            // Add complete assistant message to history using accumulated message
            setMessages((prev) => [
              ...prev,
              {
                role: 'assistant',
                content: accumulatedMessage,
                agentType: agentType as 'billing' | 'technical' | 'policy',
              },
            ]);

            // Clear streaming state
            setStreamingMessage('');
            setStreamingAgentType(undefined);
            setIsLoading(false);
          },

          onError: (errorMessage) => {
            setError(errorMessage);
            setIsLoading(false);
            setStreamingMessage('');
            setStreamingAgentType(undefined);
          },
        });
      } catch (err) {
        const errorMessage =
          err instanceof Error
            ? err.message
            : 'Failed to connect to the server. Please check your connection.';
        setError(errorMessage);
        setIsLoading(false);
        setStreamingMessage('');
        setStreamingAgentType(undefined);
      }
    },
    [isLoading, sessionId]
  );

  const handleRetry = useCallback(() => {
    if (lastUserMessage) {
      handleSendMessage(lastUserMessage);
    }
  }, [lastUserMessage, handleSendMessage]);

  return (
    <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-950">
      {/* Header */}
      <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-gray-900 dark:text-gray-100">
              Advanced Customer Service AI
            </h1>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Powered by Multi-Agent LangGraph System
            </p>
          </div>
          {sessionId && (
            <div className="text-xs text-gray-500 dark:text-gray-400 font-mono">
              Session: {sessionId.slice(0, 8)}...
            </div>
          )}
        </div>
      </header>

      {/* Message List */}
      <MessageList
        messages={messages}
        isLoading={isLoading}
        streamingMessage={streamingMessage}
        streamingAgentType={streamingAgentType}
      />

      {/* Error Display */}
      {error && (
        <div className="px-4">
          <div className="max-w-4xl mx-auto">
            <ErrorMessage message={error} onRetry={handleRetry} />
          </div>
        </div>
      )}

      {/* Chat Input */}
      <ChatInput onSend={handleSendMessage} disabled={isLoading} />
    </div>
  );
}

