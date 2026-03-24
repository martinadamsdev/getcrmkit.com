import { createFileRoute } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { parseAsInteger, parseAsString, useQueryState } from "nuqs"
import { PageContainer } from "@/shared/components/layout/page-container"
import { PageHeader } from "@/shared/components/layout/page-header"
import { OrderToolbar } from "@/features/order/components/OrderToolbar"
import { OrderTable } from "@/features/order/components/OrderTable"
import type { OrderStatus, PaymentStatus } from "@/shared/lib/constants"
import { apiFetch } from "@/shared/api/fetcher"

export const Route = createFileRoute("/_app/orders/")({
  component: OrderListPage,
})

function OrderListPage() {
  const [search, setSearch] = useQueryState("q", parseAsString.withDefault(""))
  const [orderStatus, setOrderStatus] = useQueryState("status", parseAsString)
  const [paymentStatus, setPaymentStatus] = useQueryState(
    "payment_status",
    parseAsString,
  )
  const [page, setPage] = useQueryState("page", parseAsInteger.withDefault(1))
  const [size] = useQueryState("size", parseAsInteger.withDefault(20))

  const { data } = useQuery({
    queryKey: [
      "orders",
      { search, orderStatus, paymentStatus, page, size },
    ],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (search) params.set("q", search)
      if (orderStatus) params.set("status", orderStatus)
      if (paymentStatus) params.set("payment_status", paymentStatus)
      params.set("page", String(page))
      params.set("size", String(size))
      const res = await apiFetch(`/api/v1/orders?${params}`)
      if (!res.ok) throw new Error("Failed to fetch orders")
      return res.json()
    },
    staleTime: 2 * 60 * 1000,
  })

  const orders = (data?.items ?? []).map((o: any) => ({
    id: o.id,
    orderNo: o.order_no,
    internalNo: o.internal_no,
    customerName: o.customer_name,
    totalAmount: o.total_amount,
    currency: o.currency,
    status: o.status,
    paymentStatus: o.payment_status,
    carrier: o.carrier,
    domesticTrackingNo: o.domestic_tracking_no,
    internationalTrackingNo: o.international_tracking_no,
    createdAt: o.created_at,
  }))

  return (
    <PageContainer>
      <PageHeader title="订单管理" description="管理所有销售订单" />
      <OrderToolbar
        search={search}
        onSearchChange={setSearch}
        orderStatus={orderStatus as OrderStatus | null}
        onOrderStatusChange={(s) => {
          setOrderStatus(s)
          setPage(1)
        }}
        paymentStatus={paymentStatus as PaymentStatus | null}
        onPaymentStatusChange={(s) => {
          setPaymentStatus(s)
          setPage(1)
        }}
      />
      <OrderTable
        data={orders}
        pageCount={data?.pages ?? 0}
        pagination={{ pageIndex: (page ?? 1) - 1, pageSize: size ?? 20 }}
        onPaginationChange={(p) => setPage(p.pageIndex + 1)}
      />
    </PageContainer>
  )
}
