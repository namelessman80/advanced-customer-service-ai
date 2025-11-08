/**
 * ErrorMessage Component
 * Displays error messages with optional retry functionality
 */

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

export default function ErrorMessage({ message, onRetry }: ErrorMessageProps) {
  return (
    <div className="mx-4 my-2 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
      <div className="flex items-start gap-3">
        <span className="text-xl">⚠️</span>
        <div className="flex-1">
          <h4 className="text-sm font-semibold text-red-800 dark:text-red-300 mb-1">
            Error
          </h4>
          <p className="text-sm text-red-700 dark:text-red-400">
            {message}
          </p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="mt-3 px-3 py-1.5 text-sm font-medium text-red-700 dark:text-red-300 bg-white dark:bg-red-900/30 border border-red-300 dark:border-red-700 rounded-md hover:bg-red-50 dark:hover:bg-red-900/40 transition-colors"
            >
              Try Again
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

