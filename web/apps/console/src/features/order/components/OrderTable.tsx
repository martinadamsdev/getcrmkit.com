import { useNavigate } from "@tanstack/react-router"
import type { PaginationState } from "@tanstack/react-table"
import { ShoppingCart } from "lucide-react"
import { DataTable } from "@/shared/components/data/data-table"
import { EmptyState } from "@/shared/components/data/empty-state"
import { orderColumns, type OrderRow } from "./order-columns"

interface OrderTableProps {
  data: OrderRow[]
  pageCount: number
  pagination: PaginationState
  onPaginationChange: (pagination: PaginationState) => void
}

export function OrderTable({
  data,
  pageCount,
  pagination,
  onPaginationChange,
}: OrderTableProps) {
  const navigate = useNavigate()

  if (data.length === 0) {
    return (
      <EmptyState
        icon={ShoppingCart}
        title="暂无订单"
        description="订单将在报价单确认后自动创建"
      />
    )
  }

  return (
    <DataTable
      columns={orderColumns}
      data={data}
      pagination={{
        page: pagination.pageIndex + 1,
        pageSize: pagination.pageSize,
        total: pageCount * pagination.pageSize,
      }}
      onPageChange={(page) =>
        onPaginationChange({
          pageIndex: page - 1,
          pageSize: pagination.pageSize,
        })
      }
      onRowClick={(row) =>
        navigate({ to: "/orders/$id", params: { id: row.id } })
      }
    />
  )
}
