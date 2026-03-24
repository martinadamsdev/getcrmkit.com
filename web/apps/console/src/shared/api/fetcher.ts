import { useAuthStore } from "@/shared/stores/auth.store"

let isRefreshing = false
let refreshPromise: Promise<boolean> | null = null

export async function apiFetch(url: string, init?: RequestInit): Promise<Response> {
  const token = useAuthStore.getState().accessToken
  const headers = new Headers(init?.headers)
  if (token) {
    headers.set("Authorization", `Bearer ${token}`)
  }
  if (!headers.has("Content-Type") && init?.body && !(init.body instanceof FormData)) {
    headers.set("Content-Type", "application/json")
  }
  const res = await fetch(url, { ...init, headers })
  if (res.status === 401) {
    // Don't retry auth endpoints themselves
    if (url.includes("/auth/refresh") || url.includes("/auth/login") || url.includes("/auth/register")) {
      return res
    }

    const refreshToken = useAuthStore.getState().refreshToken
    if (!refreshToken) {
      useAuthStore.getState().logout()
      window.location.href = "/login"
      return res
    }

    // Coalesce concurrent refresh requests
    if (!isRefreshing) {
      isRefreshing = true
      refreshPromise = (async () => {
        try {
          const refreshRes = await fetch("/api/v1/auth/refresh", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh_token: refreshToken }),
          })
          if (refreshRes.ok) {
            const data = await refreshRes.json()
            useAuthStore.getState().setTokens(data.access_token, data.refresh_token)
            return true
          }
        } catch {
          // Refresh failed
        }
        useAuthStore.getState().logout()
        window.location.href = "/login"
        return false
      })().finally(() => {
        isRefreshing = false
        refreshPromise = null
      })
    }

    const refreshed = await refreshPromise
    if (refreshed) {
      const newToken = useAuthStore.getState().accessToken
      headers.set("Authorization", `Bearer ${newToken}`)
      return fetch(url, { ...init, headers })
    }
  }
  return res
}
