import { useState } from "react"
import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { ArrowLeft, Users } from "lucide-react"
import { Button } from "@workspace/ui/components/button"
import { Skeleton } from "@workspace/ui/components/skeleton"
import { PageContainer } from "@/shared/components/layout/page-container"
import { EmptyState } from "@/shared/components/data/empty-state"
import { CustomerHeader } from "@/features/customer/components/customer-header"
import { Customer360Tabs } from "@/features/customer/components/customer-360-tabs"
import { apiFetch } from "@/shared/api/fetcher"
// TODO: Replace with CustomerEditDialog when available

export const Route = createFileRoute("/_app/customers/$id")({
  component: CustomerDetailPage,
})

async function fetchCustomer360(id: string) {
  const res = await apiFetch(`/api/v1/customers/${id}/360`)
  if (!res.ok) {
    if (res.status === 404) return null
    throw new Error("Failed to fetch customer")
  }
  return res.json()
}

async function deleteCustomer(id: string) {
  const res = await apiFetch(`/api/v1/customers/${id}`, { method: "DELETE" })
  if (!res.ok) throw new Error("Failed to delete customer")
}

function CustomerDetailPage() {
  const { id } = Route.useParams()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  // TODO: Implement edit dialog
  const [editDialogOpen, setEditDialogOpen] = useState(false)

  const customerQuery = useQuery({
    queryKey: ["customer-360", id],
    queryFn: () => fetchCustomer360(id),
    staleTime: 5 * 60 * 1000,
  })

  const deleteMutation = useMutation({
    mutationFn: () => deleteCustomer(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["customers"] })
      navigate({ to: "/customers" })
    },
  })

  const handleDelete = () => {
    if (window.confirm("确定要删除该客户吗？此操作不可恢复。")) {
      deleteMutation.mutate()
    }
  }

  // Loading state
  if (customerQuery.isLoading) {
    return (
      <PageContainer>
        <div className="space-y-6">
          <div className="flex items-center gap-4">
            <Skeleton className="h-10 w-10 rounded-full" />
            <div className="space-y-2">
              <Skeleton className="h-6 w-48" />
              <Skeleton className="h-4 w-32" />
            </div>
          </div>
          <Skeleton className="h-10 w-full" />
          <Skeleton className="h-64 w-full" />
        </div>
      </PageContainer>
    )
  }

  // Not found
  if (!customerQuery.data || customerQuery.isError) {
    return (
      <PageContainer>
        <EmptyState
          icon={Users}
          title="客户不存在"
          description="该客户可能已被删除或您没有访问权限"
          action={{
            label: "返回客户列表",
            onClick: () => navigate({ to: "/customers" }),
          }}
        />
      </PageContainer>
    )
  }

  const data = customerQuery.data

  return (
    <PageContainer>
      <Button
        variant="ghost"
        size="sm"
        onClick={() => navigate({ to: "/customers" })}
        className="mb-2"
      >
        <ArrowLeft className="mr-1 size-4" />
        返回列表
      </Button>

      <CustomerHeader
        customer={data.customer}
        onEdit={() => setEditDialogOpen(true)}
        onDelete={handleDelete}
      />

      <Customer360Tabs data={data} />

      {/* TODO: CustomerEditDialog — edit functionality pending */}
    </PageContainer>
  )
}
