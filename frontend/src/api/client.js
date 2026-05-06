import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 120000,
});

export const sendQuery = (query) => api.post('/query', { query });
export const queryChecklist = (query) => api.post('/query/checklist', { query });
export const uploadIncident = (file) => {
  const fd = new FormData();
  fd.append('file', file);
  return api.post('/upload/incident', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
};
export const uploadSchedule = (file) => {
  const fd = new FormData();
  fd.append('file', file);
  return api.post('/upload/schedule', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
};
export const healthCheck = () => api.get('/health');
export const getSources = () => api.get('/sources');

export default api;
