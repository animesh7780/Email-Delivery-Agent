import React, { useState } from 'react';
import { chatAPI } from '../api';

function ChatInterface() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I\'m your email assistant. I can help you analyze your inbox, prioritize tasks, and answer questions about your emails. What would you like to know?'
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || loading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    
    // Add user message to chat
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    
    try {
      setLoading(true);
      const response = await chatAPI.send(userMessage);
      
      // Add assistant response to chat
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: response.data.response 
      }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please make sure your API is configured correctly.' 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`chat-message ${message.role}`}>
            {message.content}
          </div>
        ))}
        {loading && (
          <div className="chat-message assistant">
            <em>Thinking...</em>
          </div>
        )}
      </div>
      
      <div className="chat-input-area">
        <form className="chat-input-form" onSubmit={handleSendMessage}>
          <input
            type="text"
            className="chat-input"
            placeholder="Ask me about your emails..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            disabled={loading}
          />
          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={loading || !inputMessage.trim()}
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default ChatInterface;
