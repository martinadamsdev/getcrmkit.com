import type { ColumnDef } from "@tanstack/react-table"
import { MoneyDisplay } from "@/shared/components/data/money-display"
import { OrderStatusBadge } from "./OrderStatusBadge"
import { PaymentStatusBadge } from "./PaymentStatusBadge"
import { formatDate } from "@/shared/lib/format"

export interface OrderRow {
  id: string
  orderNo: string
  internalNo: string | null
  customerName: string
  totalAmount: number
  currency: string
  status: string
  paymentStatus: string
  carrier: string | null
  domesticTrackingNo: string | null
  internationalTrackingNo: string | null
  createdAt: string
}

export const orderColumns: ColumnDef<OrderRow, unknown>[] = [
  {
    accessorKey: "orderNo",
    header: "订单号",
    cell: ({ row }) => (
      <span className="font-medium">{row.original.orderNo}</span>
    ),
  },
  {
    accessorKey: "internalNo",
    header: "内部编号",
    cell: ({ row }) => (
      <span className="text-muted-foreground">
        {row.original.internalNo ?? "—"}
      </span>
    ),
  },
  {
    accessorKey: "customerName",
    header: "客户",
  },
  {
    accessorKey: "totalAmount",
    header: "金额",
    cell: ({ row }) => (
      <MoneyDisplay
        amount={row.original.totalAmount}
        currency={row.original.currency}
      />
    ),
  },
  {
    accessorKey: "status",
    header: "订单状态",
    cell: ({ row }) => <OrderStatusBadge status={row.original.status} />,
  },
  {
    accessorKey: "paymentStatus",
    header: "付款状态",
    cell: ({ row }) => (
      <PaymentStatusBadge status={row.original.paymentStatus} />
    ),
  },
  {
    accessorKey: "carrier",
    header: "承运商",
    cell: ({ row }) => row.original.carrier ?? "—",
  },
  {
    accessorKey: "domesticTrackingNo",
    header: "国内单号",
    cell: ({ row }) => (
      <span className="font-mono text-xs">
        {row.original.domesticTrackingNo ?? "—"}
      </span>
    ),
  },
  {
    accessorKey: "internationalTrackingNo",
    header: "国际单号",
    cell: ({ row }) => (
      <span className="font-mono text-xs">
        {row.original.internationalTrackingNo ?? "—"}
      </span>
    ),
  },
  {
    accessorKey: "createdAt",
    header: "创建日期",
    cell: ({ row }) => formatDate(row.original.createdAt),
  },
]
