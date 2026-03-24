import { renderHook, act } from "@testing-library/react"
import { describe, it, expect, vi } from "vitest"
import { useFilters, type FilterDef } from "./use-filters"

// Mock nuqs to use simple state instead of URL params in tests
vi.mock("nuqs", () => {
  const { useState, useCallback } = require("react")
  return {
    parseAsString: {},
    useQueryStates: (parsers: Record<string, unknown>) => {
      const initial = Object.fromEntries(
        Object.keys(parsers).map((k) => [k, null]),
      )
      const [state, setState] = useState(initial)
      const setStateFn = useCallback(
        (updater: unknown) => {
          setState((prev: Record<string, string | null>) => {
            if (typeof updater === "function") {
              return updater(prev)
            }
            return updater
          })
        },
        [],
      )
      return [state, setStateFn]
    },
  }
})

const testFilters: FilterDef[] = [
  { key: "grade", label: "Grade", type: "select", options: [{ label: "A", value: "A" }] },
  { key: "country", label: "Country", type: "text" },
]

describe("useFilters", () => {
  it("returns empty filters by default", () => {
    const { result } = renderHook(() => useFilters(testFilters))
    expect(result.current.filters).toEqual({ grade: null, country: null })
  })

  it("setFilter updates a single filter key", () => {
    const { result } = renderHook(() => useFilters(testFilters))
    act(() => {
      result.current.setFilter("grade", "A")
    })
    expect(result.current.filters.grade).toBe("A")
    expect(result.current.filters.country).toBeNull()
  })

  it("resetFilters clears all filter values", () => {
    const { result } = renderHook(() => useFilters(testFilters))
    act(() => {
      result.current.setFilter("grade", "A")
      result.current.setFilter("country", "US")
    })
    act(() => {
      result.current.resetFilters()
    })
    expect(result.current.filters).toEqual({ grade: null, country: null })
  })

  it("preserves other filters when setting one", () => {
    const { result } = renderHook(() => useFilters(testFilters))
    act(() => {
      result.current.setFilter("grade", "A")
    })
    act(() => {
      result.current.setFilter("country", "US")
    })
    expect(result.current.filters.grade).toBe("A")
    expect(result.current.filters.country).toBe("US")
  })
})
