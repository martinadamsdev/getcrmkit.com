import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import { apiFetch } from "@/shared/api/fetcher"
import { PageContainer } from "@/shared/components/layout/page-container"
import { PageHeader } from "@/shared/components/layout/page-header"
import { QuotationEditor } from "@/features/quotation/components/quotation-editor"
import { Skeleton } from "@workspace/ui/components/skeleton"

export const Route = createFileRoute("/_app/quotations/$id")({
  component: EditQuotationPage,
})

function EditQuotationPage() {
  const { id } = Route.useParams()
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const { data, isLoading, error } = useQuery({
    queryKey: ["quotation", id],
    queryFn: async () => {
      const res = await apiFetch(`/api/v1/quotations/${id}`)
      if (!res.ok) throw new Error("Failed to fetch quotation")
      return res.json()
    },
    staleTime: 5 * 60 * 1000,
  })

  const convertMutation = useMutation({
    mutationFn: async (quotationId: string) => {
      const res = await apiFetch(
        `/api/v1/orders/from-quotation/${quotationId}`,
        { method: "POST" },
      )
      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error(err.detail ?? "Conversion failed")
      }
      return res.json()
    },
    onSuccess: (resData) => {
      toast.success(`订单 ${resData.order_no} 已创建`)
      queryClient.invalidateQueries({ queryKey: ["quotation", id] })
      queryClient.invalidateQueries({ queryKey: ["quotations"] })
      queryClient.invalidateQueries({ queryKey: ["orders"] })
      queryClient.invalidateQueries({ queryKey: ["nav-badges"] })
      navigate({ to: "/orders/$id", params: { id: resData.id } })
    },
    onError: (err) => {
      toast.error(
        err instanceof Error ? err.message : "转换订单失败",
      )
    },
  })

  if (isLoading) {
    return (
      <PageContainer>
        <Skeleton className="h-8 w-64" />
        <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-[1fr_320px]">
          <div className="space-y-6">
            <Skeleton className="h-24 w-full" />
            <Skeleton className="h-48 w-full" />
            <Skeleton className="h-64 w-full" />
          </div>
          <Skeleton className="hidden h-80 lg:block" />
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
        title={`报价 ${data?.quotation_no ?? ""}`}
        description={data?.customer_name}
      />
      <QuotationEditor
        quotationId={id}
        initialData={data}
        onConvertToOrder={(quotationId) => convertMutation.mutate(quotationId)}
        isConverting={convertMutation.isPending}
      />
    </PageContainer>
  )
}
