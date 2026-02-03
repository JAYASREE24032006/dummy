import axios from 'axios';
import { useEffect } from 'react';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

const useAuthInterceptor = (navigate) => {
  useEffect(() => {
    const interceptor = api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response && error.response.status === 401) {
          // Token expired or revoked
          console.warn("401 Detected - Logging out");
          sessionStorage.removeItem('token');
          sessionStorage.removeItem('user_id');
          navigate('/login');
        }
        return Promise.reject(error);
      }
    );

    return () => {
      api.interceptors.response.eject(interceptor);
    };
  }, [navigate]);

  return api;
};

export default useAuthInterceptor;
export { api };
