import { useCallback, useState } from "react"
import { Button } from "@workspace/ui/components/button"
import { FileText, GitCompare } from "lucide-react"
import { StatusBadge } from "@/shared/components/data/status-badge"
import { EmptyState } from "@/shared/components/data/empty-state"
import { formatDate, formatMoney } from "@/shared/lib/format"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@workspace/ui/components/table"
import { QuotationCompareView } from "./quotation-compare-view"
import type { QuotationDetail, QuotationSummary } from "../types"

type CustomerQuotationsProps = {
  quotations: QuotationSummary[]
  onRowClick?: (quotation: QuotationSummary) => void
  onLoadDetail?: (id: string) => Promise<QuotationDetail>
  className?: string
}

const QUOTATION_STATUS_LABELS: Record<string, string> = {
  draft: "草稿",
  sent: "已发送",
  following: "跟进中",
  confirmed: "已确认",
  converted: "已转换",
  expired: "已过期",
  rejected: "已拒绝",
}

export function CustomerQuotations({
  quotations,
  onRowClick,
  onLoadDetail,
  className,
}: CustomerQuotationsProps) {
  const [selectedIds, setSelectedIds] = useState<string[]>([])
  const [compareData, setCompareData] = useState<{
    a: QuotationDetail
    b: QuotationDetail
  } | null>(null)
  const [isComparing, setIsComparing] = useState(false)

  const toggleSelect = useCallback((id: string) => {
    setSelectedIds((prev) => {
      if (prev.includes(id)) {
        return prev.filter((x) => x !== id)
      }
      if (prev.length < 2) {
        return [...prev, id]
      }
      return prev
    })
  }, [])

  const handleCompare = async () => {
    if (selectedIds.length !== 2 || !onLoadDetail) return
    setIsComparing(true)
    try {
      const [a, b] = await Promise.all([
        onLoadDetail(selectedIds[0]),
        onLoadDetail(selectedIds[1]),
      ])
      setCompareData({ a, b })
    } finally {
      setIsComparing(false)
    }
  }

  if (compareData) {
    return (
      <div className={className}>
        <div className="mb-4">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setCompareData(null)}
          >
            返回列表
          </Button>
        </div>
        <QuotationCompareView
          quotationA={compareData.a}
          quotationB={compareData.b}
        />
      </div>
    )
  }

  if (quotations.length === 0) {
    return (
      <div className={className}>
        <EmptyState
          icon={FileText}
          title="暂无报价"
          description="还没有相关报价记录"
        />
      </div>
    )
  }

  return (
    <div className={className}>
      {selectedIds.length > 0 && (
        <div className="mb-3 flex items-center gap-2">
          <span className="text-sm text-muted-foreground">
            已选 {selectedIds.length} 项
          </span>
          <Button
            size="sm"
            variant="outline"
            disabled={selectedIds.length !== 2 || isComparing}
            onClick={handleCompare}
          >
            <GitCompare className="mr-2 size-4" />
            {isComparing ? "加载中..." : "对比报价"}
          </Button>
        </div>
      )}
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead />
            <TableHead>报价编号</TableHead>
            <TableHead>金额</TableHead>
            <TableHead>贸易条款</TableHead>
            <TableHead>状态</TableHead>
            <TableHead>日期</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {quotations.map((q) => (
            <TableRow
              key={q.id}
              className={onRowClick ? "cursor-pointer" : ""}
              onClick={() => onRowClick?.(q)}
            >
              <TableCell>
                <input
                  type="checkbox"
                  checked={selectedIds.includes(q.id)}
                  onChange={() => toggleSelect(q.id)}
                  onClick={(e) => e.stopPropagation()}
                  aria-label={`Select ${q.quotation_no}`}
                  className="size-4 cursor-pointer"
                />
              </TableCell>
              <TableCell className="font-medium">{q.quotation_no}</TableCell>
              <TableCell>{formatMoney(q.total_amount, q.currency)}</TableCell>
              <TableCell>{q.trade_terms ?? "—"}</TableCell>
              <TableCell>
                <StatusBadge
                  status={q.status}
                  labelMap={QUOTATION_STATUS_LABELS}
                />
              </TableCell>
              <TableCell>{formatDate(q.created_at)}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
