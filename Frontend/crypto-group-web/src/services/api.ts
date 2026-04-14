import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'
import type { TokenResponse } from '@/types/auth.types'

const baseURL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api/v1'

export const api = axios.create({
  baseURL,
  timeout: 120_000,
})

const refreshClient = axios.create({
  baseURL,
  timeout: 30_000,
})

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (r) => r,
  async (error) => {
    const original = error.config
    if (!original || original._retry) {
      return Promise.reject(error)
    }
    if (error.response?.status !== 401) {
      return Promise.reject(error)
    }
    const url = String(original.url ?? '')
    if (url.includes('/auth/login') || url.includes('/auth/register') || url.includes('/auth/refresh')) {
      return Promise.reject(error)
    }
    const refresh = useAuthStore.getState().refreshToken
    if (!refresh) {
      useAuthStore.getState().logout()
      return Promise.reject(error)
    }
    original._retry = true
    try {
      const { data } = await refreshClient.post<TokenResponse>('/auth/refresh', {
        refresh_token: refresh,
      })
      useAuthStore.getState().setTokens(data.access_token, data.refresh_token)
      original.headers.Authorization = `Bearer ${data.access_token}`
      return api(original)
    } catch {
      useAuthStore.getState().logout()
      return Promise.reject(error)
    }
  },
)

export { baseURL }
