/**
 * MessageList Component
 * Displays conversation history with auto-scroll
 */

'use client';

import { useEffect, useRef } from 'react';
import Message from './Message';
import LoadingIndicator from './LoadingIndicator';

interface MessageData {
  role: 'user' | 'assistant';
  content: string;
  agentType?: 'billing' | 'technical' | 'policy';
}

interface MessageListProps {
  messages: MessageData[];
  isLoading: boolean;
  streamingMessage?: string;
  streamingAgentType?: 'billing' | 'technical' | 'policy';
}

export default function MessageList({
  messages,
  isLoading,
  streamingMessage,
  streamingAgentType,
}: MessageListProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom - simple and reliable
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, streamingMessage]);

  return (
    <div
      ref={scrollRef}
      className="flex-1 overflow-y-auto px-4 py-6 space-y-4"
      style={{ minHeight: 0 }}
    >
      <div className="max-w-4xl mx-auto">
      {messages.length === 0 && !isLoading && (
        <div className="flex flex-col items-center justify-center min-h-[400px] text-center px-4">
          <div className="mb-4 text-6xl">💬</div>
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
            Welcome to Advanced Customer Service AI
          </h2>
          <p className="text-gray-600 dark:text-gray-400 max-w-md">
            Ask me anything about billing, technical support, or our policies.
            I'll route your question to the right specialist!
          </p>
          <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-3 max-w-2xl w-full">
            <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
              <div className="text-2xl mb-1">💰</div>
              <div className="text-xs font-medium text-blue-900 dark:text-blue-300">
                Billing
              </div>
              <div className="text-xs text-blue-700 dark:text-blue-400 mt-1">
                Pricing, invoices, subscriptions
              </div>
            </div>
            <div className="p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg border border-orange-200 dark:border-orange-800">
              <div className="text-2xl mb-1">🔧</div>
              <div className="text-xs font-medium text-orange-900 dark:text-orange-300">
                Technical Support
              </div>
              <div className="text-xs text-orange-700 dark:text-orange-400 mt-1">
                Issues, bugs, integrations
              </div>
            </div>
            <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
              <div className="text-2xl mb-1">📋</div>
              <div className="text-xs font-medium text-green-900 dark:text-green-300">
                Policy & Compliance
              </div>
              <div className="text-xs text-green-700 dark:text-green-400 mt-1">
                Privacy, terms, GDPR
              </div>
            </div>
          </div>
        </div>
      )}

      {messages.map((msg, index) => (
        <Message
          key={index}
          role={msg.role}
          content={msg.content}
          agentType={msg.agentType}
        />
      ))}

      {/* Streaming message (assistant is typing) */}
      {streamingMessage && (
        <Message
          role="assistant"
          content={streamingMessage}
          agentType={streamingAgentType}
        />
      )}

      {/* Loading indicator */}
      {isLoading && !streamingMessage && <LoadingIndicator />}
      </div>
    </div>
  );
}

