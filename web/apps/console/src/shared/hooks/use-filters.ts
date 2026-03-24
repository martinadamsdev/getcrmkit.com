import { parseAsString, useQueryStates } from "nuqs"

export type FilterDef = {
  key: string
  label: string
  type: "text" | "select" | "multi-select"
  options?: { label: string; value: string }[]
}

export function useFilters(filterDefs: FilterDef[]) {
  const parsers = Object.fromEntries(
    filterDefs.map((f) => [f.key, parseAsString]),
  )
  const [filters, setFilters] = useQueryStates(parsers)

  const setFilter = (key: string, value: string | null) => {
    setFilters((prev) => ({ ...prev, [key]: value }))
  }

  const resetFilters = () => {
    setFilters(Object.fromEntries(filterDefs.map((f) => [f.key, null])))
  }

  return { filters, setFilter, resetFilters }
}
