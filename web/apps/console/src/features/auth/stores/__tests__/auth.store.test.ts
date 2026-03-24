import { describe, it, expect, beforeEach } from "vitest"
import { useAuthStore } from "../auth.store"

describe("Auth Store", () => {
  beforeEach(() => {
    // Clear persisted state and reset store
    useAuthStore.persist.clearStorage()
    useAuthStore.setState({
      accessToken: null,
      refreshToken: null,
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
    })
  })

  it("should start unauthenticated", () => {
    const state = useAuthStore.getState()
    expect(state.isAuthenticated).toBe(false)
    expect(state.accessToken).toBeNull()
    expect(state.refreshToken).toBeNull()
    expect(state.user).toBeNull()
  })

  it("should set tokens and mark as authenticated", () => {
    useAuthStore.getState().setTokens("access_123", "refresh_456")
    const state = useAuthStore.getState()
    expect(state.isAuthenticated).toBe(true)
    expect(state.accessToken).toBe("access_123")
    expect(state.refreshToken).toBe("refresh_456")
  })

  it("should store user profile", () => {
    const user = {
      id: "uuid-1",
      email: "test@example.com",
      name: "Test User",
      timezone: "Asia/Shanghai",
      language: "zh-CN",
      role: "owner",
      last_login_at: null,
      created_at: "2026-01-01T00:00:00Z",
    }
    useAuthStore.getState().setUser(user)
    expect(useAuthStore.getState().user).toEqual(user)
  })

  it("should clear all state on logout", () => {
    useAuthStore.getState().setTokens("access_123", "refresh_456")
    useAuthStore.getState().logout()
    const state = useAuthStore.getState()
    expect(state.isAuthenticated).toBe(false)
    expect(state.accessToken).toBeNull()
    expect(state.refreshToken).toBeNull()
    expect(state.user).toBeNull()
  })

  it("should derive isAuthenticated from accessToken presence", () => {
    expect(useAuthStore.getState().isAuthenticated).toBe(false)
    useAuthStore.getState().setTokens("tok", "ref")
    expect(useAuthStore.getState().isAuthenticated).toBe(true)
    useAuthStore.getState().setTokens(null, null)
    expect(useAuthStore.getState().isAuthenticated).toBe(false)
  })

  it("should update only access token on refresh", () => {
    useAuthStore.getState().setTokens("old_access", "old_refresh")
    useAuthStore.getState().setTokens("new_access", "new_refresh")
    const state = useAuthStore.getState()
    expect(state.accessToken).toBe("new_access")
    expect(state.refreshToken).toBe("new_refresh")
  })

  it("should reset to initial state", () => {
    useAuthStore.getState().setTokens("a", "r")
    useAuthStore.getState().setUser({ id: "1" } as any)
    useAuthStore.getState().reset()
    const state = useAuthStore.getState()
    expect(state.accessToken).toBeNull()
    expect(state.user).toBeNull()
    expect(state.isAuthenticated).toBe(false)
  })

  it("should track loading state", () => {
    expect(useAuthStore.getState().isLoading).toBe(false)
    useAuthStore.getState().setLoading(true)
    expect(useAuthStore.getState().isLoading).toBe(true)
  })
})
