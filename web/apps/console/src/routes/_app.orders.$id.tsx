import { createFileRoute } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { PageContainer } from "@/shared/components/layout/page-container"
import { PageHeader } from "@/shared/components/layout/page-header"
import { OrderDetail } from "@/features/order/components/OrderDetail"
import { Skeleton } from "@workspace/ui/components/skeleton"
import { apiFetch } from "@/shared/api/fetcher"

export const Route = createFileRoute("/_app/orders/$id")({
  component: OrderDetailPage,
})

function OrderDetailPage() {
  const { id } = Route.useParams()

  const { data, isLoading, error } = useQuery({
    queryKey: ["order", id],
    queryFn: async () => {
      const res = await apiFetch(`/api/v1/orders/${id}`)
      if (!res.ok) throw new Error("Failed to fetch order")
      return res.json()
    },
    staleTime: 5 * 60 * 1000,
  })

  if (isLoading) {
    return (
      <PageContainer>
        <Skeleton className="h-8 w-64" />
        <div className="mt-6 space-y-6">
          <Skeleton className="h-32 w-full" />
          <Skeleton className="h-48 w-full" />
          <div className="grid grid-cols-2 gap-6">
            <Skeleton className="h-48 w-full" />
            <Skeleton className="h-48 w-full" />
          </div>
        </div>
      </PageContainer>
    )
  }

  if (error) {
    return (
      <PageContainer>
        <div className="text-destructive">加载失败: {error.message}</div>
      </PageContainer>
    )
  }

  return (
    <PageContainer>
      <PageHeader
        title={`订单 ${data?.order_no ?? ""}`}
        description={data?.customer_name}
      />
      <OrderDetail order={data} />
    </PageContainer>
  )
}
