import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table"
import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "@workspace/ui/components/avatar"
import { Badge } from "@workspace/ui/components/badge"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@workspace/ui/components/table"
import { Package } from "lucide-react"

interface ProductRow {
  id: string
  name: string
  sku: string | null
  category_name: string | null
  image_url: string | null
  cost_price: string | null
  cost_currency: string
  selling_price: string | null
  selling_currency: string
  variant_count: number
  is_active: boolean
  created_at: string
}

interface ProductTableProps {
  data: ProductRow[]
  total: number
  page: number
  pageSize: number
  onPageChange: (page: number) => void
  onRowClick: (productId: string) => void
}

const CURRENCY_SYMBOLS: Record<string, string> = {
  CNY: "¥",
  USD: "$",
  EUR: "€",
  GBP: "£",
}

function formatPrice(amount: string | null, currency: string): string {
  if (!amount) return "\u2014"
  const symbol = CURRENCY_SYMBOLS[currency] ?? currency
  return `${symbol}${amount}`
}

const columnHelper = createColumnHelper<ProductRow>()

const columns = [
  columnHelper.display({
    id: "product",
    header: "产品",
    cell: ({ row }) => (
      <div className="flex items-center gap-3">
        <Avatar className="h-9 w-9 rounded-md">
          {row.original.image_url ? (
            <AvatarImage
              src={row.original.image_url}
              alt={row.original.name}
            />
          ) : null}
          <AvatarFallback className="rounded-md">
            <Package className="h-4 w-4 text-muted-foreground" />
          </AvatarFallback>
        </Avatar>
        <span className="font-medium truncate max-w-[200px]">
          {row.original.name}
        </span>
      </div>
    ),
  }),
  columnHelper.accessor("sku", {
    header: "SKU",
    cell: (info) => (
      <span className="font-mono text-xs text-muted-foreground">
        {info.getValue() ?? "\u2014"}
      </span>
    ),
  }),
  columnHelper.accessor("category_name", {
    header: "分类",
    cell: (info) => (
      <Badge variant="outline" className="text-xs">
        {info.getValue() ?? "未分类"}
      </Badge>
    ),
  }),
  columnHelper.display({
    id: "cost",
    header: "成本",
    cell: ({ row }) => (
      <span className="text-sm">
        {formatPrice(row.original.cost_price, row.original.cost_currency)}
      </span>
    ),
  }),
  columnHelper.display({
    id: "selling",
    header: "售价",
    cell: ({ row }) => (
      <span className="text-sm font-medium">
        {formatPrice(
          row.original.selling_price,
          row.original.selling_currency,
        )}
      </span>
    ),
  }),
  columnHelper.accessor("variant_count", {
    header: "变体",
    cell: (info) => (
      <span className="text-sm text-muted-foreground">{info.getValue()}</span>
    ),
  }),
]

export function ProductTable({
  data,
  total,
  page,
  pageSize,
  onPageChange,
  onRowClick,
}: ProductTableProps) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  })

  const totalPages = Math.ceil(total / pageSize)

  return (
    <div>
      <Table>
        <TableHeader>
          {table.getHeaderGroups().map((hg) => (
            <TableRow key={hg.id}>
              {hg.headers.map((h) => (
                <TableHead key={h.id}>
                  {h.isPlaceholder
                    ? null
                    : flexRender(h.column.columnDef.header, h.getContext())}
                </TableHead>
              ))}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {table.getRowModel().rows.length === 0 ? (
            <TableRow>
              <TableCell
                colSpan={columns.length}
                className="h-24 text-center text-muted-foreground"
              >
                暂无产品
              </TableCell>
            </TableRow>
          ) : (
            table.getRowModel().rows.map((row) => (
              <TableRow
                key={row.id}
                className="cursor-pointer"
                onClick={() => onRowClick(row.original.id)}
              >
                {row.getVisibleCells().map((cell) => (
                  <TableCell key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </TableCell>
                ))}
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
      {totalPages > 1 && (
        <div className="flex items-center justify-between border-t px-4 py-3">
          <span className="text-sm text-muted-foreground">
            共 {total} 个产品
          </span>
          <div className="flex gap-1">
            <button
              type="button"
              disabled={page <= 1}
              onClick={() => onPageChange(page - 1)}
              className="rounded px-3 py-1 text-sm disabled:opacity-50"
            >
              上一页
            </button>
            <span className="px-3 py-1 text-sm">
              {page} / {totalPages}
            </span>
            <button
              type="button"
              disabled={page >= totalPages}
              onClick={() => onPageChange(page + 1)}
              className="rounded px-3 py-1 text-sm disabled:opacity-50"
            >
              下一页
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
