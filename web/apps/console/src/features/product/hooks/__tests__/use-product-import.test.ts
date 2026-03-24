import { describe, expect, it, vi, beforeEach } from "vitest"

describe("useProductImport", () => {
  beforeEach(() => {
    global.fetch = vi.fn()
  })

  it("should be importable", async () => {
    const { useProductImport } = await import("../use-product-import")
    expect(useProductImport).toBeDefined()
  })
})
