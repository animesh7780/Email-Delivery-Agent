import React, { useState, useEffect } from 'react';
import { emailAPI, draftAPI } from '../api';

function EmailDetail({ email, onClose, onProcessComplete }) {
  const [processing, setProcessing] = useState(false);
  const [processedEmail, setProcessedEmail] = useState(email);
  const [drafts, setDrafts] = useState([]);
  const [showDraft, setShowDraft] = useState(false);

  useEffect(() => {
    loadDrafts();
  }, [email.id]);

  const loadDrafts = async () => {
    try {
      const response = await draftAPI.getAll(email.id);
      setDrafts(response.data);
    } catch (error) {
      console.error('Error loading drafts:', error);
    }
  };

  const handleProcess = async (tasks) => {
    try {
      setProcessing(true);
      const response = await emailAPI.process(email.id, { email_id: email.id, tasks });
      setProcessedEmail(response.data.email);
      if (tasks.includes('generate_draft')) {
        await loadDrafts();
        setShowDraft(true);
      }
      onProcessComplete();
    } catch (error) {
      console.error('Error processing email:', error);
      alert('Error processing email. Please check your API configuration.');
    } finally {
      setProcessing(false);
    }
  };

  const parseActionItems = () => {
    if (!processedEmail.action_items) return [];
    try {
      return JSON.parse(processedEmail.action_items);
    } catch {
      return [];
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">Email Details</h2>
          <button className="close-btn" onClick={onClose}>&times;</button>
        </div>

        <div className="email-detail">
          <div className="email-detail-header">
            <h3 className="email-detail-subject">{processedEmail.subject}</h3>
            <div className="email-detail-from">
              From: <strong>{processedEmail.sender_name}</strong> &lt;{processedEmail.sender}&gt;
            </div>
            <div className="email-meta" style={{marginTop: '10px'}}>
              <span className="badge badge-category">{processedEmail.category}</span>
              <span className={`badge badge-priority ${processedEmail.priority.toLowerCase()}`}>
                {processedEmail.priority}
              </span>
              {processedEmail.sentiment && (
                <span className="badge" style={{backgroundColor: '#9b59b6', color: 'white'}}>
                  {processedEmail.sentiment}
                </span>
              )}
            </div>
          </div>

          <div className="email-detail-body">
            {processedEmail.body}
          </div>

          {processedEmail.has_action_items && parseActionItems().length > 0 && (
            <div className="action-items">
              <h4>📋 Action Items</h4>
              <ul>
                {parseActionItems().map((item, index) => (
                  <li key={index}>
                    <strong>{item.task || item}</strong>
                    {item.deadline && <span> - Due: {item.deadline}</span>}
                    {item.priority && (
                      <span className={`badge badge-priority ${item.priority.toLowerCase()}`} 
                            style={{marginLeft: '10px'}}>
                        {item.priority}
                      </span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="button-group">
            <button 
              className="btn btn-primary" 
              onClick={() => handleProcess(['categorize', 'extract_tasks'])}
              disabled={processing}
            >
              {processing ? '⏳ Processing...' : '🤖 Analyze Email'}
            </button>
            <button 
              className="btn btn-success" 
              onClick={() => handleProcess(['categorize', 'extract_tasks', 'generate_draft'])}
              disabled={processing}
            >
              {processing ? '⏳ Processing...' : '✍️ Generate Draft Reply'}
            </button>
          </div>

          {showDraft && drafts.length > 0 && (
            <div style={{marginTop: '30px', padding: '20px', backgroundColor: '#e8f5e9', borderRadius: '8px'}}>
              <h4 style={{marginBottom: '15px', color: '#2e7d32'}}>📝 Draft Reply</h4>
              <div style={{marginBottom: '10px'}}>
                <strong>Subject:</strong> {drafts[drafts.length - 1].subject}
              </div>
              <div style={{backgroundColor: 'white', padding: '15px', borderRadius: '5px', whiteSpace: 'pre-wrap'}}>
                {drafts[drafts.length - 1].body}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default EmailDetail;
