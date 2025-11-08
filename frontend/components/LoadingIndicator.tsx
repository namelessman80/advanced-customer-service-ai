/**
 * LoadingIndicator Component
 * Animated typing indicator (bouncing dots)
 */

export default function LoadingIndicator() {
  return (
    <div className="flex items-center gap-1 px-4 py-3">
      <div className="flex gap-1">
        <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
        <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
        <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce"></div>
      </div>
      <span className="ml-2 text-sm text-gray-500 dark:text-gray-400">
        AI is thinking...
      </span>
    </div>
  );
}

