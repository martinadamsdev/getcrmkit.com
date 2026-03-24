import { Link } from "@tanstack/react-router"
import { Plus } from "lucide-react"
import { Button } from "@workspace/ui/components/button"
import {
  ToggleGroup,
  ToggleGroupItem,
} from "@workspace/ui/components/toggle-group"
import { SearchInput } from "@/shared/components/form/search-input"
import { QUOTATION_STATUSES, type QuotationStatus } from "@/shared/lib/constants"

type QuotationToolbarProps = {
  search: string
  onSearchChange: (value: string) => void
  status: QuotationStatus | null
  onStatusChange: (status: QuotationStatus | null) => void
}

export function QuotationToolbar({
  search,
  onSearchChange,
  status,
  onStatusChange,
}: QuotationToolbarProps) {
  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <SearchInput
          placeholder="搜索报价编号、客户..."
          onSearch={onSearchChange}
          defaultValue={search}
          className="w-80"
        />
        <Button asChild>
          <Link to="/quotations/new">
            <Plus className="mr-2 size-4" />
            新建报价
          </Link>
        </Button>
      </div>
      <ToggleGroup
        type="single"
        value={status ?? "all"}
        onValueChange={(val) => {
          onStatusChange(val === "all" ? null : (val as QuotationStatus))
        }}
      >
        <ToggleGroupItem value="all" aria-label="显示全部">
          全部
        </ToggleGroupItem>
        {QUOTATION_STATUSES.map((s) => (
          <ToggleGroupItem key={s.value} value={s.value} aria-label={s.label}>
            {s.label}
          </ToggleGroupItem>
        ))}
      </ToggleGroup>
    </div>
  )
}
