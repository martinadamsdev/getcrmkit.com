import { create } from "zustand"
import { persist } from "zustand/middleware"

export interface AuthUser {
  id: string
  email: string
  name: string
  timezone: string
  language: string
  role: string
  last_login_at: string | null
  created_at: string
}

interface AuthState {
  accessToken: string | null
  refreshToken: string | null
  user: AuthUser | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null

  setTokens: (accessToken: string | null, refreshToken: string | null) => void
  setUser: (user: AuthUser | null) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  logout: () => void
  reset: () => void
}

const initialState = {
  accessToken: null as string | null,
  refreshToken: null as string | null,
  user: null as AuthUser | null,
  isAuthenticated: false,
  isLoading: false,
  error: null as string | null,
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      ...initialState,

      setTokens: (accessToken, refreshToken) =>
        set({
          accessToken,
          refreshToken,
          isAuthenticated: accessToken !== null,
        }),

      setUser: (user) => set({ user }),

      setLoading: (isLoading) => set({ isLoading }),

      setError: (error) => set({ error }),

      logout: () => set({ ...initialState }),

      reset: () => set({ ...initialState }),
    }),
    {
      name: "crmkit-auth",
      partialize: (state) => ({ refreshToken: state.refreshToken }),
    },
  ),
)
