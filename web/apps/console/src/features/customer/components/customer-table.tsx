import type { ColumnDef, SortingState } from "@tanstack/react-table"
import { Badge } from "@workspace/ui/components/badge"
import { Users } from "lucide-react"
import { DataTable } from "@/shared/components/data/data-table"
import { GradeBadge } from "@/shared/components/business/grade-badge"
import { CountryFlag } from "@/shared/components/business/country-flag"
import { formatRelativeTime } from "@/shared/lib/format"
import type { CustomerResponse } from "../types"

type CustomerTableProps = {
  data: CustomerResponse[]
  pagination: { page: number; pageSize: number; total: number }
  onPageChange: (page: number) => void
  sorting?: SortingState
  onSortingChange?: (sorting: SortingState) => void
  onRowClick?: (customer: CustomerResponse) => void
  isLoading?: boolean
}

const columns: ColumnDef<CustomerResponse, unknown>[] = [
  {
    accessorKey: "name",
    header: "公司名",
    cell: ({ row }) => (
      <span className="font-medium">{row.original.name}</span>
    ),
    enableSorting: true,
  },
  {
    accessorKey: "country",
    header: "国家",
    cell: ({ row }) => (
      <CountryFlag countryCode={row.original.country} showName />
    ),
    enableSorting: true,
  },
  {
    id: "grade",
    header: "等级",
    cell: ({ row }) =>
      row.original.grade ? (
        <GradeBadge
          grade={row.original.grade.name}
          color={row.original.grade.color}
        />
      ) : (
        <span className="text-muted-foreground">—</span>
      ),
    enableSorting: false,
  },
  {
    id: "tags",
    header: "标签",
    cell: ({ row }) => (
      <div className="flex flex-wrap gap-1">
        {row.original.tags.map((tag) => (
          <Badge
            key={tag.id}
            variant="secondary"
            style={{ backgroundColor: tag.color, color: "#fff" }}
          >
            {tag.name}
          </Badge>
        ))}
      </div>
    ),
    enableSorting: false,
  },
  {
    accessorKey: "source",
    header: "来源",
    enableSorting: true,
  },
  {
    accessorKey: "last_follow_at",
    header: "最近跟进",
    cell: ({ row }) =>
      row.original.last_follow_at ? (
        <span>{formatRelativeTime(row.original.last_follow_at)}</span>
      ) : (
        <span className="text-muted-foreground">—</span>
      ),
    enableSorting: true,
  },
  {
    accessorKey: "contact_count",
    header: "联系人数",
    cell: ({ row }) => (
      <span>{row.original.contact_count}</span>
    ),
    enableSorting: false,
  },
]

export function CustomerTable({
  data,
  pagination,
  onPageChange,
  sorting,
  onSortingChange,
  onRowClick,
  isLoading,
}: CustomerTableProps) {
  return (
    <DataTable<CustomerResponse>
      columns={columns}
      data={data}
      pagination={pagination}
      onPageChange={onPageChange}
      sorting={sorting}
      onSortingChange={onSortingChange}
      onRowClick={onRowClick}
      isLoading={isLoading}
      emptyState={{
        icon: Users,
        title: "暂无客户",
        description: "点击「新建客户」添加你的第一个客户",
      }}
    />
  )
}
