import React from 'react';

export function Welcome() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[85vh] text-gray-500 dark:text-gray-400 space-y-6">
      <div className="w-24 h-24 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center">
        <span className="text-4xl">🎬</span>
      </div>
      <h2 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600">
        Film Chat APP
      </h2>
      <p className="text-center text-sm max-w-md px-4">
        Welcome! I can analyze your movie reviews in two ways:
        <br />
        🎭 Sentiment Analysis - Understand the emotional tone
        <br />
        🎯 Topic Analysis - Identify the main themes
      </p>
    </div>
  );
}
