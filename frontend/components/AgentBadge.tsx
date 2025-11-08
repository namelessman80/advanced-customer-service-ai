/**
 * AgentBadge Component
 * Displays which agent is responding (Billing, Technical, or Policy)
 */

interface AgentBadgeProps {
  agentType: 'billing' | 'technical' | 'policy';
}

export default function AgentBadge({ agentType }: AgentBadgeProps) {
  const agentConfig = {
    billing: {
      emoji: '💰',
      label: 'Billing',
      bgColor: 'bg-blue-100 dark:bg-blue-900/30',
      textColor: 'text-blue-700 dark:text-blue-300',
      borderColor: 'border-blue-200 dark:border-blue-800',
    },
    technical: {
      emoji: '🔧',
      label: 'Technical Support',
      bgColor: 'bg-orange-100 dark:bg-orange-900/30',
      textColor: 'text-orange-700 dark:text-orange-300',
      borderColor: 'border-orange-200 dark:border-orange-800',
    },
    policy: {
      emoji: '📋',
      label: 'Policy & Compliance',
      bgColor: 'bg-green-100 dark:bg-green-900/30',
      textColor: 'text-green-700 dark:text-green-300',
      borderColor: 'border-green-200 dark:border-green-800',
    },
  };

  const config = agentConfig[agentType];

  return (
    <div
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border ${config.bgColor} ${config.textColor} ${config.borderColor}`}
    >
      <span className="text-sm">{config.emoji}</span>
      <span>{config.label}</span>
    </div>
  );
}

