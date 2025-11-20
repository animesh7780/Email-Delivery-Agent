import React from 'react';

function EmailList({ emails, onEmailClick }) {
  if (emails.length === 0) {
    return (
      <div className="empty-state">
        <h3>No emails found</h3>
        <p>Your inbox is empty or no emails match the current filter.</p>
      </div>
    );
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  const truncateText = (text, maxLength = 100) => {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
  };

  return (
    <div className="email-list">
      {emails.map((email) => (
        <div 
          key={email.id} 
          className={`email-card ${!email.is_read ? 'unread' : ''}`}
          onClick={() => onEmailClick(email)}
        >
          <div className="email-header">
            <span className="email-sender">{email.sender_name}</span>
            <span className="email-time">{formatDate(email.received_at)}</span>
          </div>
          <div className="email-subject">{email.subject}</div>
          <div className="email-preview">{truncateText(email.body)}</div>
          <div className="email-meta">
            <span className="badge badge-category">{email.category}</span>
            <span className={`badge badge-priority ${email.priority.toLowerCase()}`}>
              {email.priority}
            </span>
            {email.has_action_items && (
              <span className="badge" style={{backgroundColor: '#f39c12', color: 'white'}}>
                📋 Has Tasks
              </span>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

export default EmailList;
