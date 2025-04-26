import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
});

api.interceptors.request.use(async (config) => {
  let token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }
        const response = await axios.post('http://127.0.0.1:8000/api/token/refresh/', {
          refresh: refreshToken,
        });
        const newAccessToken = response.data.access;
        localStorage.setItem('access_token', newAccessToken);
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export const login = async (username, password) => {
  const response = await api.post('token/', { username, password });
  localStorage.setItem('access_token', response.data.access);
  localStorage.setItem('refresh_token', response.data.refresh);
  return response;
};

export const getAppointments = () => {
  return api.get('appointments/');
};

export const createAppointment = (data) => {
  return api.post('appointments/', data);
};

export const getMedicalRecord = () => {
  return api.get('patients/me/');
};

export const getPatientProfile = () => {
  return api.get('patients/me/');
};

export const updatePatientProfile = (data) => {
  return api.patch('patients/me/', data);
};

export const getDicomImages = () => {
  return api.get('orthanc/patients/');
};

export const uploadDicomFile = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('orthanc/dicom-to-png/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    responseType: 'arraybuffer',
  });
};