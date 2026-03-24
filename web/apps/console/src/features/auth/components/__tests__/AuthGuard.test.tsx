import { describe, it, expect, beforeEach } from "vitest"
import { useAuthStore } from "../../stores/auth.store"

describe("AuthGuard (beforeLoad logic)", () => {
  beforeEach(() => {
    useAuthStore.getState().reset()
  })

  it("should detect unauthenticated state", () => {
    const { isAuthenticated } = useAuthStore.getState()
    expect(isAuthenticated).toBe(false)
  })

  it("should detect authenticated state", () => {
    useAuthStore.getState().setTokens("token", "refresh")
    const { isAuthenticated } = useAuthStore.getState()
    expect(isAuthenticated).toBe(true)
  })
})
