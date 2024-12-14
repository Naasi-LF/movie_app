import React from 'react';

export function InputArea({ 
  message, 
  setMessage, 
  handleSubmit, 
  isLoading, 
  analysisType, 
  setAnalysisType,
  modelMenuOpen,
  setModelMenuOpen 
}) {
  return (
    <div className="border-t border-gray-200 dark:border-gray-600 bg-white dark:bg-[#343541] p-4">
      <div className="max-w-3xl mx-auto">
        <form onSubmit={handleSubmit} className="flex items-center gap-4">
          <div className="relative">
            <button
              type="button"
              onClick={() => setModelMenuOpen(!modelMenuOpen)}
              className="h-10 w-10 rounded-lg bg-blue-100 dark:bg-blue-900 hover:bg-blue-200 dark:hover:bg-blue-800 flex items-center justify-center text-blue-600 dark:text-blue-400"
            >
              {analysisType === 'sentiment' ? '🎭' : '🎯'}
            </button>
            
            {modelMenuOpen && (
              <div className="absolute bottom-full mb-2 left-0 w-48 rounded-lg shadow-lg bg-white dark:bg-gray-800 ring-1 ring-black ring-opacity-5 z-10">
                <div className="py-1">
                  <button
                    type="button"
                    onClick={() => {
                      setAnalysisType('sentiment');
                      setModelMenuOpen(false);
                    }}
                    className={`block px-4 py-2 text-sm w-full text-left ${
                      analysisType === 'sentiment'
                        ? 'bg-blue-50 dark:bg-blue-900 text-blue-700 dark:text-blue-200'
                        : 'text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700'
                    }`}
                  >
                    🎭 Sentiment Analysis
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setAnalysisType('topic');
                      setModelMenuOpen(false);
                    }}
                    className={`block px-4 py-2 text-sm w-full text-left ${
                      analysisType === 'topic'
                        ? 'bg-blue-50 dark:bg-blue-900 text-blue-700 dark:text-blue-200'
                        : 'text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700'
                    }`}
                  >
                    🎯 Topic Analysis
                  </button>
                </div>
              </div>
            )}
          </div>
          
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your movie review here..."
            className="flex-1 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 px-4 py-2 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={isLoading || !message.trim()}
            className="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-500 to-blue-600 text-white font-medium hover:from-blue-600 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
