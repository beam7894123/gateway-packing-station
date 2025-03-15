import axios from 'axios';
import store from '../store';

const apiService = axios.create({
  baseURL: import.meta.env.VITE_BASE_API_URL,
  timeout: 10000,
});

apiService.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      store.dispatch({ type: 'addAlert', alert: { type: 'danger', message: 'API ERROR: Request timed out!' } });
    } else {
      store.dispatch({ type: 'addAlert', alert: { type: 'danger', message: 'API ERROR: An error occurred!' } });
    }
    return Promise.reject(error);
  }
);

export default apiService;