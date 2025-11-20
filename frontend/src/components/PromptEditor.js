import React, { useState, useEffect } from 'react';
import { promptAPI } from '../api';

function PromptEditor() {
  const [prompts, setPrompts] = useState([]);
  const [editingPrompt, setEditingPrompt] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    prompt_type: 'categorization',
    content: '',
    is_active: true
  });

  useEffect(() => {
    loadPrompts();
  }, []);

  const loadPrompts = async () => {
    try {
      const response = await promptAPI.getAll();
      setPrompts(response.data);
    } catch (error) {
      console.error('Error loading prompts:', error);
    }
  };

  const handleEdit = (prompt) => {
    setEditingPrompt(prompt);
    setFormData({
      name: prompt.name,
      prompt_type: prompt.prompt_type,
      content: prompt.content,
      is_active: prompt.is_active
    });
    setShowForm(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingPrompt) {
        await promptAPI.update(editingPrompt.id, formData);
      } else {
        await promptAPI.create(formData);
      }
      setShowForm(false);
      setEditingPrompt(null);
      setFormData({
        name: '',
        prompt_type: 'categorization',
        content: '',
        is_active: true
      });
      loadPrompts();
    } catch (error) {
      console.error('Error saving prompt:', error);
      alert('Error saving prompt. Please check if the name is unique.');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this prompt?')) {
      try {
        await promptAPI.delete(id);
        loadPrompts();
      } catch (error) {
        console.error('Error deleting prompt:', error);
      }
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingPrompt(null);
    setFormData({
      name: '',
      prompt_type: 'categorization',
      content: '',
      is_active: true
    });
  };

  if (showForm) {
    return (
      <div>
        <h3>{editingPrompt ? 'Edit Prompt' : 'Create New Prompt'}</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Prompt Name</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              required
              disabled={!!editingPrompt}
            />
          </div>

          <div className="form-group">
            <label>Prompt Type</label>
            <select
              value={formData.prompt_type}
              onChange={(e) => setFormData({...formData, prompt_type: e.target.value})}
              required
            >
              <option value="categorization">Categorization</option>
              <option value="task_extraction">Task Extraction</option>
              <option value="auto_reply">Auto Reply</option>
            </select>
          </div>

          <div className="form-group">
            <label>Prompt Content</label>
            <textarea
              value={formData.content}
              onChange={(e) => setFormData({...formData, content: e.target.value})}
              required
              placeholder="Enter your prompt template here. Use {subject} and {body} as placeholders."
            />
          </div>

          <div className="form-group">
            <label>
              <input
                type="checkbox"
                checked={formData.is_active}
                onChange={(e) => setFormData({...formData, is_active: e.target.checked})}
              />
              {' '}Active
            </label>
          </div>

          <div className="button-group">
            <button type="submit" className="btn btn-primary">Save Prompt</button>
            <button type="button" className="btn btn-secondary" onClick={handleCancel}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    );
  }

  return (
    <div>
      <div style={{marginBottom: '20px'}}>
        <button className="btn btn-primary" onClick={() => setShowForm(true)}>
          + Create New Prompt
        </button>
      </div>

      {prompts.length === 0 ? (
        <div className="empty-state">
          <h3>No prompts configured</h3>
          <p>Create your first prompt template to customize AI behavior.</p>
        </div>
      ) : (
        <div className="prompt-list">
          {prompts.map((prompt) => (
            <div key={prompt.id} className="prompt-card">
              <h3>{prompt.name}</h3>
              <span className="prompt-type">{prompt.prompt_type}</span>
              {prompt.is_active && (
                <span className="badge" style={{backgroundColor: '#27ae60', color: 'white', marginLeft: '10px'}}>
                  Active
                </span>
              )}
              <div className="prompt-content">{prompt.content}</div>
              <div className="button-group">
                <button className="btn btn-primary" onClick={() => handleEdit(prompt)}>
                  Edit
                </button>
                <button className="btn btn-secondary" onClick={() => handleDelete(prompt.id)}>
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default PromptEditor;
