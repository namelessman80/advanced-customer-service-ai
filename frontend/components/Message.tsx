/**
 * Message Component
 * Displays individual user or assistant messages
 */

import AgentBadge from './AgentBadge';

interface MessageProps {
  role: 'user' | 'assistant';
  content: string;
  agentType?: 'billing' | 'technical' | 'policy';
}

export default function Message({ role, content, agentType }: MessageProps) {
  const isUser = role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          isUser
            ? 'bg-blue-600 text-white rounded-br-sm'
            : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 rounded-bl-sm'
        }`}
      >
        {/* Agent Badge for assistant messages */}
        {!isUser && agentType && (
          <div className="mb-2">
            <AgentBadge agentType={agentType} />
          </div>
        )}

        {/* Message content */}
        <div className="whitespace-pre-wrap text-sm leading-relaxed">
          {content}
        </div>
      </div>
    </div>
  );
}

