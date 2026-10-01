import { createContext, useContext, useEffect, useState } from 'react'
import api from './api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem('eh_user')) } catch { return null }
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('eh_access')
    if (!token) return setLoading(false)
    api.get('/auth/me/')
      .then(({ data }) => {
        setUser(data)
        localStorage.setItem('eh_user', JSON.stringify(data))
      })
      .catch(() => {
        localStorage.removeItem('eh_access')
        localStorage.removeItem('eh_refresh')
        localStorage.removeItem('eh_user')
        setUser(null)
      })
      .finally(() => setLoading(false))
  }, [])

  const login = async (username, password) => {
    const { data } = await api.post('/auth/login/', { username, password })
    localStorage.setItem('eh_access', data.access)
    localStorage.setItem('eh_refresh', data.refresh)
    localStorage.setItem('eh_user', JSON.stringify(data.user))
    setUser(data.user)
    return data.user
  }

  const register = async (payload) => {
    await api.post('/auth/register/', payload)
    return login(payload.username, payload.password)
  }

  const logout = async () => {
    try {
      const refresh = localStorage.getItem('eh_refresh')
      if (refresh) await api.post('/auth/logout/', { refresh })
    } catch {}
    localStorage.removeItem('eh_access')
    localStorage.removeItem('eh_refresh')
    localStorage.removeItem('eh_user')
    setUser(null)
  }

  return <AuthContext.Provider value={{ user, loading, login, register, logout }}>
    {children}
  </AuthContext.Provider>
}

export const useAuth = () => useContext(AuthContext)
