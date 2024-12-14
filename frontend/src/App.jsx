import { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { ChatArea } from './components/ChatArea';
import { InputArea } from './components/InputArea';

export default function App() {
  const [message, setMessage] = useState('');
  const [analysisType, setAnalysisType] = useState('sentiment');
  const [isLoading, setIsLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [darkMode, setDarkMode] = useState(true);
  const [modelMenuOpen, setModelMenuOpen] = useState(false);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    const newMessage = {
      type: 'user',
      content: message,
      analysisType
    };
    setChatHistory([...chatHistory, newMessage]);
    setMessage('');
    setIsLoading(true);

    try {
      const res = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: newMessage.content,
          analysis_type: analysisType,
        }),
      });
      const data = await res.json();
      
      setChatHistory(prev => [...prev, {
        type: 'assistant',
        content: data.gpt_analysis.gpt_text
      }]);
    } catch (error) {
      console.error('Error:', error);
      setChatHistory(prev => [...prev, {
        type: 'assistant',
        content: 'Sorry, something went wrong. Please try again.'
      }]);
    }
    setIsLoading(false);
  };

  return (
    <div className={`h-screen flex flex-col ${darkMode ? 'dark' : ''}`}>
      <Header darkMode={darkMode} setDarkMode={setDarkMode} />
      <ChatArea chatHistory={chatHistory} isLoading={isLoading} />
      <InputArea
        message={message}
        setMessage={setMessage}
        handleSubmit={handleSubmit}
        isLoading={isLoading}
        analysisType={analysisType}
        setAnalysisType={setAnalysisType}
        modelMenuOpen={modelMenuOpen}
        setModelMenuOpen={setModelMenuOpen}
      />
    </div>
  );
}
