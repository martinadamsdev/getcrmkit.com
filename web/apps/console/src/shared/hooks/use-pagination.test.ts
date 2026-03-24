import { renderHook, act } from "@testing-library/react"
import { describe, it, expect, vi } from "vitest"
import { usePagination } from "./use-pagination"

// Mock nuqs to use simple state instead of URL params in tests
vi.mock("nuqs", () => {
  const { useState } = require("react")
  return {
    parseAsInteger: {
      withDefault: (defaultValue: number) => defaultValue,
    },
    useQueryState: (_key: string, defaultValue: number) => {
      return useState(defaultValue)
    },
  }
})

describe("usePagination", () => {
  it("returns default page=1, pageSize=20", () => {
    const { result } = renderHook(() => usePagination())
    expect(result.current.page).toBe(1)
    expect(result.current.pageSize).toBe(20)
  })

  it("setPage updates page value", () => {
    const { result } = renderHook(() => usePagination())
    act(() => {
      result.current.setPage(3)
    })
    expect(result.current.page).toBe(3)
  })

  it("setPageSize resets page to 1", () => {
    const { result } = renderHook(() => usePagination())
    act(() => {
      result.current.setPage(5)
    })
    expect(result.current.page).toBe(5)
    act(() => {
      result.current.setPageSize(50)
    })
    expect(result.current.pageSize).toBe(50)
    expect(result.current.page).toBe(1)
  })

  it("computes offset correctly: (page - 1) * pageSize", () => {
    const { result } = renderHook(() => usePagination())
    act(() => {
      result.current.setPage(3)
    })
    expect(result.current.offset).toBe(40) // (3 - 1) * 20
  })
})
