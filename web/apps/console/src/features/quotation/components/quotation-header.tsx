import { Input } from "@workspace/ui/components/input"
import { StatusBadge } from "@/shared/components/data/status-badge"
import { QUOTATION_STATUS_MAP } from "@/shared/lib/constants"

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

type QuotationHeaderProps = {
  quotationNo: string
  onQuotationNoChange: (value: string) => void
  status: string
  isNew?: boolean
}

export function QuotationHeader({
  quotationNo,
  onQuotationNoChange,
  status,
  isNew = false,
}: QuotationHeaderProps) {
  return (
    <div className="flex items-center gap-4">
      <div className="flex-1">
        <label className="text-sm font-medium text-muted-foreground">
          报价编号
        </label>
        <Input
          value={quotationNo}
          onChange={(e) => onQuotationNoChange(e.target.value)}
          placeholder="QUOT-2026-001"
          className="mt-1 text-lg font-semibold"
        />
      </div>
      {!isNew && (
        <StatusBadge
          status={status}
          colorMap={quotationColorMap}
          labelMap={quotationLabelMap}
        />
      )}
    </div>
  )
}
