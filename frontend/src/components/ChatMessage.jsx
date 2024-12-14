import React from 'react';

export function ChatMessage({ message }) {
  return (
    <div
      className={`border-b border-gray-200 dark:border-gray-600/50 ${
        message.type === 'user' ? 'bg-white dark:bg-[#343541]' : 'bg-gray-50 dark:bg-[#444654]'
      }`}
    >
      <div className="max-w-3xl mx-auto flex gap-6 p-6">
        {message.type === 'user' ? (
          <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-blue-500 to-blue-600 flex items-center justify-center flex-shrink-0 text-white">
            👤
          </div>
        ) : (
          <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-green-500 to-teal-500 flex items-center justify-center flex-shrink-0">
            🤖
          </div>
        )}
        <div className="flex-1 space-y-2 overflow-hidden">
          <p className="font-medium text-sm text-gray-800 dark:text-gray-200">
            {message.type === 'user' ? 'You' : 'Assistant'}
            {message.type === 'user' && (
              <span className="ml-2 text-xs text-gray-500 dark:text-gray-400">
                ({message.analysisType} analysis)
              </span>
            )}
          </p>
          <div className="prose dark:prose-invert max-w-none">
            <p className="leading-7">{message.content}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
