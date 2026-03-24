import { renderHook, waitFor } from "@testing-library/react"
import { describe, expect, it } from "vitest"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { http, HttpResponse } from "msw"
import { setupServer } from "msw/node"
import type { ReactNode } from "react"

import { useNavBadges } from "./use-nav-badges"

const MOCK_BADGES = {
  customers: 42,
  quotations: 5,
  orders: 3,
  follow_ups: 8,
}

const server = setupServer(
  http.get("/api/v1/nav/badges", () => HttpResponse.json(MOCK_BADGES)),
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe("useNavBadges", () => {
  function wrapper({ children }: { children: ReactNode }) {
    const queryClient = new QueryClient({
      defaultOptions: { queries: { retry: false } },
    })
    return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  }

  it("returns badge counts", async () => {
    const { result } = renderHook(() => useNavBadges(), { wrapper })
    await waitFor(() => {
      expect(result.current.customers).toBe(42)
      expect(result.current.quotations).toBe(5)
      expect(result.current.orders).toBe(3)
      expect(result.current.follow_ups).toBe(8)
    })
  })

  it("returns zero counts when fetch fails", async () => {
    server.use(
      http.get("/api/v1/nav/badges", () => new HttpResponse(null, { status: 500 })),
    )
    const { result } = renderHook(() => useNavBadges(), { wrapper })
    // Should return default zeros
    expect(result.current.customers).toBe(0)
    expect(result.current.quotations).toBe(0)
  })
})
