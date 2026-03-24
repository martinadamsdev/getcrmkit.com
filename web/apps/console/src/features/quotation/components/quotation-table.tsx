import type { ColumnDef, SortingState } from "@tanstack/react-table"
import { useNavigate } from "@tanstack/react-router"
import { FileText } from "lucide-react"
import { DataTable } from "@/shared/components/data/data-table"
import { StatusBadge } from "@/shared/components/data/status-badge"
import { formatMoney, formatDate } from "@/shared/lib/format"
import { QUOTATION_STATUS_MAP } from "@/shared/lib/constants"

export type QuotationRow = {
  id: string
  quotationNo: string
  customerName: string
  totalAmount: number
  currency: string
  tradeTerm: string
  status: string
  createdAt: string
}

const quotationColorMap: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
  draft: "secondary",
  sent: "default",
  following: "default",
  confirmed: "default",
  converted: "default",
  expired: "secondary",
  rejected: "destructive",
}

const quotationLabelMap: Record<string, string> = Object.fromEntries(
  Object.entries(QUOTATION_STATUS_MAP).map(([key, val]) => [key, val.label]),
)

const columns: ColumnDef<QuotationRow, unknown>[] = [
  {
    accessorKey: "quotationNo",
    header: "编号",
    cell: ({ row }) => (
      <span className="font-medium">{row.original.quotationNo}</span>
    ),
    enableSorting: true,
  },
  {
    accessorKey: "customerName",
    header: "客户",
    enableSorting: true,
  },
  {
    accessorKey: "totalAmount",
    header: "金额",
    cell: ({ row }) => (
      <span className="tabular-nums">
        {formatMoney(row.original.totalAmount, row.original.currency)}
      </span>
    ),
    enableSorting: true,
  },
  {
    accessorKey: "currency",
    header: "币种",
    cell: ({ row }) => (
      <span className="text-xs font-medium text-muted-foreground">
        {row.original.currency}
      </span>
    ),
    enableSorting: false,
  },
  {
    accessorKey: "status",
    header: "状态",
    cell: ({ row }) => (
      <StatusBadge
        status={row.original.status}
        colorMap={quotationColorMap}
        labelMap={quotationLabelMap}
      />
    ),
    enableSorting: false,
  },
  {
    accessorKey: "createdAt",
    header: "创建时间",
    cell: ({ row }) => formatDate(row.original.createdAt),
    enableSorting: true,
  },
]

type QuotationTableProps = {
  data: QuotationRow[]
  pagination: { page: number; pageSize: number; total: number }
  onPageChange: (page: number) => void
  sorting?: SortingState
  onSortingChange?: (sorting: SortingState) => void
  isLoading?: boolean
}

export function QuotationTable({
  data,
  pagination,
  onPageChange,
  sorting,
  onSortingChange,
  isLoading,
}: QuotationTableProps) {
  const navigate = useNavigate()

  return (
    <DataTable<QuotationRow>
      columns={columns}
      data={data}
      pagination={pagination}
      onPageChange={onPageChange}
      sorting={sorting}
      onSortingChange={onSortingChange}
      onRowClick={(row) =>
        navigate({ to: "/quotations/$id", params: { id: row.id } })
      }
      isLoading={isLoading}
      emptyState={{
        icon: FileText,
        title: "暂无报价",
        description: "创建第一个报价单开始管理您的业务",
      }}
    />
  )
}
