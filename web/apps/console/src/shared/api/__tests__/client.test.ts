import { describe, it, expect } from "vitest"

describe("API Client", () => {
  it("should export a configured client instance", async () => {
    const { client } = await import("../client")
    expect(client).toBeDefined()
  })

  it("should use /api base URL", async () => {
    const { client } = await import("../client")
    const config = client.getConfig()
    expect(config.baseUrl).toBe("/api")
  })
})
