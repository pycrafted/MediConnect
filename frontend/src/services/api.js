import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
});

api.interceptors.request.use(async (config) => {
  const token = localStorage.getItem('access_token');
  console.log('Token utilisé pour la requête:', token ? 'Présent' : 'Absent', 'URL:', config.url);
  if (token && config.url !== 'token/') {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry && originalRequest.url !== 'token/') {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        console.log('Tentative de rafraîchissement du token, refresh_token:', refreshToken ? 'Présent' : 'Absent');
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }
        const response = await axios.post('http://127.0.0.1:8000/api/token/refresh/', {
          refresh: refreshToken,
        });
        const newAccessToken = response.data.access;
        console.log('Nouveau token obtenu:', newAccessToken ? 'Succès' : 'Échec');
        localStorage.setItem('access_token', newAccessToken);
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        console.error('Échec du rafraîchissement du token:', refreshError);
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
  console.log('Réponse login:', response.data);
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
  return api.get('orthanc/images/');
};

export const uploadDicomFile = (formData) => {
  return api.post('orthanc/dicom-to-png/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    responseType: 'arraybuffer',
  });
};