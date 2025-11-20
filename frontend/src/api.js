import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Email API
export const emailAPI = {
  getAll: (category = null) => {
    const params = category ? { category } : {};
    return api.get('/api/emails', { params });
  },
  getById: (id) => api.get(`/api/emails/${id}`),
  create: (email) => api.post('/api/emails', email),
  markRead: (id) => api.put(`/api/emails/${id}/read`),
  process: (id, data) => api.post(`/api/emails/${id}/process`, data),
};

// Prompt API
export const promptAPI = {
  getAll: () => api.get('/api/prompts'),
  getById: (id) => api.get(`/api/prompts/${id}`),
  create: (prompt) => api.post('/api/prompts', prompt),
  update: (id, prompt) => api.put(`/api/prompts/${id}`, prompt),
  delete: (id) => api.delete(`/api/prompts/${id}`),
};

// Draft API
export const draftAPI = {
  getAll: (emailId = null) => {
    const params = emailId ? { email_id: emailId } : {};
    return api.get('/api/drafts', { params });
  },
  getById: (id) => api.get(`/api/drafts/${id}`),
};

// Chat API
export const chatAPI = {
  send: (message, context = null) => api.post('/api/chat', { message, context }),
};

// Stats API
export const statsAPI = {
  get: () => api.get('/api/stats'),
};

export default api;
