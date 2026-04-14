import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AuthState {
  accessToken: string | null
  refreshToken: string | null
  username: string | null
  setTokens: (access: string, refresh: string) => void
  setUsername: (name: string | null) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      accessToken: null,
      refreshToken: null,
      username: null,
      setTokens: (access, refresh) =>
        set({ accessToken: access, refreshToken: refresh }),
      setUsername: (name) => set({ username: name }),
      logout: () =>
        set({ accessToken: null, refreshToken: null, username: null }),
    }),
    {
      name: 'cryptougroup-auth',
      partialize: (s) => ({
        accessToken: s.accessToken,
        refreshToken: s.refreshToken,
        username: s.username,
      }),
    },
  ),
)
