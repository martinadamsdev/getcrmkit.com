import { parseAsInteger, useQueryState } from "nuqs"

export function usePagination(defaultPageSize = 20) {
  const [page, setPageRaw] = useQueryState(
    "page",
    parseAsInteger.withDefault(1),
  )
  const [pageSize, setPageSizeRaw] = useQueryState(
    "size",
    parseAsInteger.withDefault(defaultPageSize),
  )

  const offset = (page - 1) * pageSize

  const setPage = (value: number) => {
    setPageRaw(value)
  }

  const setPageSize = (value: number) => {
    setPageSizeRaw(value)
    setPageRaw(1)
  }

  return { page, pageSize, offset, setPage, setPageSize }
}
