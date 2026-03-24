import { useAuthStore } from "@/shared/stores/auth.store"
import { refreshTokens } from "@/features/auth/api/auth.api"
import { client } from "./client"

let isRefreshing = false
let refreshPromise: Promise<void> | null = null

/**
 * Setup auth interceptor:
 * 1. Request interceptor: attach Bearer token
 * 2. Response interceptor: 401 -> silent refresh -> retry -> fail -> redirect /login
 */
export function setupAuthInterceptor(): void {
  // Request interceptor: attach Bearer token
  client.interceptors.request.use((request) => {
    const { accessToken } = useAuthStore.getState()
    if (accessToken && !request.headers.get("Authorization")) {
      request.headers.set("Authorization", `Bearer ${accessToken}`)
    }
    return request
  })

  // Response interceptor: handle 401
  client.interceptors.response.use(async (response) => {
    if (response.status !== 401) {
      return response
    }

    // Don't retry auth endpoints themselves
    const url = new URL(response.url, window.location.origin)
    if (
      url.pathname.includes("/auth/refresh") ||
      url.pathname.includes("/auth/login") ||
      url.pathname.includes("/auth/register")
    ) {
      return response
    }

    const { refreshToken } = useAuthStore.getState()
    if (!refreshToken) {
      useAuthStore.getState().logout()
      window.location.href = "/login"
      return response
    }

    // Coalesce concurrent refresh requests
    if (!isRefreshing) {
      isRefreshing = true
      refreshPromise = refreshTokens(refreshToken)
        .then((tokens) => {
          useAuthStore.getState().setTokens(tokens.access_token, tokens.refresh_token)
        })
        .catch(() => {
          useAuthStore.getState().logout()
          window.location.href = "/login"
        })
        .finally(() => {
          isRefreshing = false
          refreshPromise = null
        })
    }

    await refreshPromise

    // Token refreshed — the caller should retry the request.
    // The request interceptor will attach the new token automatically.
    return response
  })
}
