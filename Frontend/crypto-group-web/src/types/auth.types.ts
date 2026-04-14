export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  full_name?: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface RefreshTokenRequest {
  refresh_token: string
}

export interface UserResponse {
  id: string
  username: string
  email: string
  full_name: string | null
  is_active: boolean
  is_superuser: boolean
  created_at: string | null
  last_login_at: string | null
}

export interface MessageResponse {
  message: string
  success?: boolean
}
