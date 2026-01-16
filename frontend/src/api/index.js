import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || '/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_URL}/token/refresh/`, {
            refresh: refreshToken
          })

          localStorage.setItem('access_token', response.data.access)
          api.defaults.headers.Authorization = `Bearer ${response.data.access}`

          return api(originalRequest)
        } catch (refreshError) {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
      }
    }

    return Promise.reject(error)
  }
)

export default api

export const authApi = {
  login: (username, password) =>
    axios.post(`${API_URL}/token/`, { username, password }),

  register: (data) =>
    api.post('/users/register/', data),

  getProfile: () =>
    api.get('/users/profile/'),

  updateProfile: (data) =>
    api.patch('/users/profile/', data)
}

export const examsApi = {
  getCategories: () =>
    api.get('/exams/categories/'),

  getTests: () =>
    api.get('/exams/tests/'),

  startTest: (testId) =>
    api.post(`/exams/tests/${testId}/start/`),

  getAttemptQuestions: (attemptId) =>
    api.get(`/exams/attempts/${attemptId}/questions/`),

  submitAnswer: (attemptId, data) =>
    api.post(`/exams/attempts/${attemptId}/submit/`, data),

  finishTest: (attemptId) =>
    api.post(`/exams/attempts/${attemptId}/finish/`),

  getAttemptResult: (attemptId) =>
    api.get(`/exams/attempts/${attemptId}/result/`),

  getMyAttempts: () =>
    api.get('/exams/attempts/')
}

export const modulesApi = {
  getSections: () =>
    api.get('/modules/sections/'),

  getSectionsWithModules: () =>
    api.get('/modules/sections/with-modules/'),

  getSection: (id) =>
    api.get(`/modules/sections/${id}/`),

  getModules: (sectionId = null) =>
    api.get('/modules/', { params: sectionId ? { section: sectionId } : {} }),

  getModule: (id) =>
    api.get(`/modules/${id}/`),

  startModule: (moduleId) =>
    api.post(`/modules/${moduleId}/start/`),

  updateProgress: (moduleId, data) =>
    api.patch(`/modules/${moduleId}/progress/`, data),

  completeModule: (moduleId) =>
    api.post(`/modules/${moduleId}/complete/`),

  getMyProgress: () =>
    api.get('/modules/my-progress/')
}
