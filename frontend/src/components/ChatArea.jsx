import React from 'react';
import { Welcome } from './Welcome';
import { ChatMessage } from './ChatMessage';

export function ChatArea({ chatHistory, isLoading }) {
  return (
    <div className="flex-1 overflow-y-auto bg-white dark:bg-[#343541]">
      <div className="max-w-3xl mx-auto">
        {chatHistory.length === 0 && <Welcome />}
        {chatHistory.map((message, index) => (
          <ChatMessage key={index} message={message} />
        ))}
        {isLoading && (
          <div className="bg-gray-50 dark:bg-[#444654] border-b border-gray-200 dark:border-gray-600/50">
            <div className="max-w-3xl mx-auto flex gap-6 p-6">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-green-500 to-teal-500 flex items-center justify-center flex-shrink-0">
                🤖
              </div>
              <div className="flex-1">
                <p className="font-medium text-sm text-gray-800 dark:text-gray-200 mb-2">Assistant</p>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"></div>
                  <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce [animation-delay:0.2s]"></div>
                  <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce [animation-delay:0.4s]"></div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
