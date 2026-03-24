import { createFileRoute } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { parseAsInteger, parseAsString, useQueryState } from "nuqs"
import { PageContainer } from "@/shared/components/layout/page-container"
import { PageHeader } from "@/shared/components/layout/page-header"
import { QuotationToolbar } from "@/features/quotation/components/quotation-toolbar"
import { QuotationTable } from "@/features/quotation/components/quotation-table"
import type { QuotationStatus } from "@/shared/lib/constants"
import { apiFetch } from "@/shared/api/fetcher"

export const Route = createFileRoute("/_app/quotations/")({
  component: QuotationListPage,
})

function QuotationListPage() {
  const [search, setSearch] = useQueryState("q", parseAsString.withDefault(""))
  const [status, setStatus] = useQueryState("status", parseAsString)
  const [page, setPage] = useQueryState("page", parseAsInteger.withDefault(1))
  const [size] = useQueryState("size", parseAsInteger.withDefault(20))

  const { data } = useQuery({
    queryKey: ["quotations", { search, status, page, size }],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (search) params.set("q", search)
      if (status) params.set("status", status)
      params.set("page", String(page))
      params.set("size", String(size))
      const res = await apiFetch(`/api/v1/quotations?${params}`)
      if (!res.ok) throw new Error("Failed to fetch quotations")
      return res.json()
    },
    staleTime: 2 * 60 * 1000,
  })

  const quotations = (data?.items ?? []).map((q: any) => ({
    id: q.id,
    quotationNo: q.quotation_no,
    customerName: q.customer_name,
    totalAmount: q.total_amount,
    currency: q.currency,
    tradeTerm: q.trade_term,
    status: q.status,
    createdAt: q.created_at,
  }))

  return (
    <PageContainer>
      <PageHeader title="报价管理" description="管理所有报价单" />
      <QuotationToolbar
        search={search}
        onSearchChange={setSearch}
        status={status as QuotationStatus | null}
        onStatusChange={(s) => {
          setStatus(s)
          setPage(1)
        }}
      />
      <QuotationTable
        data={quotations}
        pagination={{
          page: page ?? 1,
          pageSize: size ?? 20,
          total: data?.total ?? 0,
        }}
        onPageChange={setPage}
      />
    </PageContainer>
  )
}
