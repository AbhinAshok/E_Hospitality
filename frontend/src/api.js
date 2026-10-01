import axios from 'axios'

export const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api'

const api = axios.create({ baseURL: API_URL })

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('eh_access')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  response => response,
  async error => {
    const original = error.config
    const refresh = localStorage.getItem('eh_refresh')
    if (error.response?.status === 401 && refresh && !original?._retry) {
      original._retry = true
      try {
        const { data } = await axios.post(`${API_URL}/auth/refresh/`, { refresh })
        localStorage.setItem('eh_access', data.access)
        original.headers.Authorization = `Bearer ${data.access}`
        return api(original)
      } catch {
        localStorage.removeItem('eh_access')
        localStorage.removeItem('eh_refresh')
        localStorage.removeItem('eh_user')
      }
    }
    return Promise.reject(error)
  }
)

export default api
