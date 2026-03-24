import { describe, it, expect, beforeAll, beforeEach, afterAll, afterEach } from "vitest"
import { http, HttpResponse } from "msw"
import { setupServer } from "msw/node"
import { client } from "@/shared/api/client"

const server = setupServer()

beforeAll(() => {
  server.listen()
  // In test (Node.js) environment, baseUrl must be absolute
  client.setConfig({ baseUrl: "http://localhost/api" })
})
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe("Auth API", () => {
  it("login should return tokens on success", async () => {
    server.use(
      http.post("http://localhost/api/v1/auth/login", () =>
        HttpResponse.json({
          access_token: "access_123",
          refresh_token: "refresh_456",
          token_type: "bearer",
          expires_in: 3600,
        })
      )
    )

    const { login } = await import("../auth.api")
    const result = await login({ email: "test@example.com", password: "password123", remember_me: false })
    expect(result.access_token).toBe("access_123")
    expect(result.refresh_token).toBe("refresh_456")
  })

  it("login should throw on 401", async () => {
    server.use(
      http.post("http://localhost/api/v1/auth/login", () =>
        HttpResponse.json(
          { code: "INVALID_CREDENTIALS", message: "Invalid credentials" },
          { status: 401 }
        )
      )
    )

    const { login } = await import("../auth.api")
    await expect(login({ email: "test@example.com", password: "wrong", remember_me: false })).rejects.toThrow()
  })

  it("register should return user on success", async () => {
    server.use(
      http.post("http://localhost/api/v1/auth/register", () =>
        HttpResponse.json(
          { id: "uuid-1", email: "new@example.com", name: "New User" },
          { status: 201 }
        )
      )
    )

    const { register } = await import("../auth.api")
    const result = await register({ email: "new@example.com", password: "password123", name: "New User" })
    expect(result.id).toBe("uuid-1")
  })

  it("refreshTokens should return new token pair", async () => {
    server.use(
      http.post("http://localhost/api/v1/auth/refresh", () =>
        HttpResponse.json({
          access_token: "new_access",
          refresh_token: "new_refresh",
          token_type: "bearer",
          expires_in: 3600,
        })
      )
    )

    const { refreshTokens } = await import("../auth.api")
    const result = await refreshTokens("old_refresh")
    expect(result.access_token).toBe("new_access")
  })
})
