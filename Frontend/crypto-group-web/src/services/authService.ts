import { api } from '@/services/api'
import type {
  LoginRequest,
  MessageResponse,
  RegisterRequest,
  TokenResponse,
  UserResponse,
} from '@/types/auth.types'

export async function login(body: LoginRequest): Promise<TokenResponse> {
  const { data } = await api.post<TokenResponse>('/auth/login', body)
  return data
}

export async function register(body: RegisterRequest): Promise<MessageResponse> {
  const { data } = await api.post<MessageResponse>('/auth/register', body)
  return data
}

export async function fetchMe(): Promise<UserResponse> {
  const { data } = await api.get<UserResponse>('/auth/me')
  return data
}
