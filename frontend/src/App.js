import React, { useState, useEffect } from 'react';
import './App.css';
import EmailList from './components/EmailList';
import EmailDetail from './components/EmailDetail';
import PromptEditor from './components/PromptEditor';
import ChatInterface from './components/ChatInterface';
import { emailAPI, statsAPI } from './api';

function App() {
  const [currentView, setCurrentView] = useState('inbox');
  const [emails, setEmails] = useState([]);
  const [selectedEmail, setSelectedEmail] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState(null);

  useEffect(() => {
    loadEmails();
    loadStats();
  }, [selectedCategory]);

  const loadEmails = async () => {
    try {
      setLoading(true);
      const response = await emailAPI.getAll(selectedCategory);
      setEmails(response.data);
    } catch (error) {
      console.error('Error loading emails:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const response = await statsAPI.get();
      setStats(response.data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const handleEmailClick = async (email) => {
    setSelectedEmail(email);
    if (!email.is_read) {
      await emailAPI.markRead(email.id);
      loadEmails();
      loadStats();
    }
  };

  const handleCategoryClick = (category) => {
    setSelectedCategory(category);
    setCurrentView('inbox');
  };

  const handleProcessComplete = () => {
    loadEmails();
    loadStats();
  };

  const renderContent = () => {
    switch (currentView) {
      case 'inbox':
        return (
          <>
            <div className="header">
              <h2>{selectedCategory || 'All Emails'}</h2>
              {stats && (
                <div className="stats-bar">
                  <div className="stat-card">
                    <strong>Total:</strong> {stats.total_emails}
                  </div>
                  <div className="stat-card">
                    <strong>Unread:</strong> {stats.unread_count}
                  </div>
                  <div className="stat-card">
                    <strong>Action Items:</strong> {stats.action_items_count}
                  </div>
                  <div className="stat-card">
                    <strong>Drafts:</strong> {stats.drafts_count}
                  </div>
                </div>
              )}
            </div>
            <div className="content-area">
              {loading ? (
                <div className="loading">Loading emails...</div>
              ) : (
                <EmailList emails={emails} onEmailClick={handleEmailClick} />
              )}
            </div>
          </>
        );
      
      case 'prompts':
        return (
          <>
            <div className="header">
              <h2>Prompt Configuration</h2>
            </div>
            <div className="content-area">
              <PromptEditor />
            </div>
          </>
        );
      
      case 'chat':
        return (
          <>
            <div className="header">
              <h2>Chat with AI Assistant</h2>
            </div>
            <div className="content-area">
              <ChatInterface />
            </div>
          </>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="app">
      <div className="sidebar">
        <h1>📧 Email Agent</h1>
        <ul className="nav-menu">
          <li 
            className={`nav-item ${currentView === 'inbox' && !selectedCategory ? 'active' : ''}`}
            onClick={() => { setCurrentView('inbox'); setSelectedCategory(null); }}
          >
            All Emails
            {stats && <span className="category-badge">{stats.total_emails}</span>}
          </li>
          
          <li 
            className={`nav-item ${currentView === 'inbox' && selectedCategory === 'Work' ? 'active' : ''}`}
            onClick={() => handleCategoryClick('Work')}
          >
            Work
            {stats && stats.categories.Work && <span className="category-badge">{stats.categories.Work}</span>}
          </li>
          
          <li 
            className={`nav-item ${currentView === 'inbox' && selectedCategory === 'Important' ? 'active' : ''}`}
            onClick={() => handleCategoryClick('Important')}
          >
            Important
            {stats && stats.categories.Important && <span className="category-badge">{stats.categories.Important}</span>}
          </li>
          
          <li 
            className={`nav-item ${currentView === 'inbox' && selectedCategory === 'Personal' ? 'active' : ''}`}
            onClick={() => handleCategoryClick('Personal')}
          >
            Personal
            {stats && stats.categories.Personal && <span className="category-badge">{stats.categories.Personal}</span>}
          </li>
          
          <li 
            className={`nav-item ${currentView === 'inbox' && selectedCategory === 'Promotional' ? 'active' : ''}`}
            onClick={() => handleCategoryClick('Promotional')}
          >
            Promotional
            {stats && stats.categories.Promotional && <span className="category-badge">{stats.categories.Promotional}</span>}
          </li>
          
          <li 
            className={`nav-item ${currentView === 'prompts' ? 'active' : ''}`}
            onClick={() => setCurrentView('prompts')}
          >
            ⚙️ Prompts
          </li>
          
          <li 
            className={`nav-item ${currentView === 'chat' ? 'active' : ''}`}
            onClick={() => setCurrentView('chat')}
          >
            💬 AI Chat
          </li>
        </ul>
      </div>

      <div className="main-content">
        {renderContent()}
      </div>

      {selectedEmail && (
        <EmailDetail 
          email={selectedEmail} 
          onClose={() => setSelectedEmail(null)}
          onProcessComplete={handleProcessComplete}
        />
      )}
    </div>
  );
}

export default App;
