import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import * as authService from '@/services/authService'
import { useAuthStore } from '@/stores/authStore'
import type { LoginRequest, RegisterRequest } from '@/types/auth.types'
import { getErrorMessage } from '@/lib/utils'

export function useLogin() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const setTokens = useAuthStore((s) => s.setTokens)
  const setUsername = useAuthStore((s) => s.setUsername)

  return useMutation({
    mutationFn: async (body: LoginRequest) => {
      const tokens = await authService.login(body)
      setTokens(tokens.access_token, tokens.refresh_token)
      const me = await authService.fetchMe()
      setUsername(me.username)
      return me
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['me'] })
      navigate('/app/inicio', { replace: true })
    },
    onError: () => {
      /* toast handled in UI */
    },
  })
}

export function useRegister() {
  const navigate = useNavigate()
  return useMutation({
    mutationFn: (body: RegisterRequest) => authService.register(body),
    onSuccess: () => {
      navigate('/login', { replace: true })
    },
  })
}

export function useLogout() {
  const navigate = useNavigate()
  const logout = useAuthStore((s) => s.logout)
  return () => {
    logout()
    navigate('/login', { replace: true })
  }
}

export function useMe() {
  const token = useAuthStore((s) => s.accessToken)
  return useQuery({
    queryKey: ['me', token],
    queryFn: () => authService.fetchMe(),
    enabled: !!token,
  })
}

export { getErrorMessage }
