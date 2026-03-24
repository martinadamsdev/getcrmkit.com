import {
  ToggleGroup,
  ToggleGroupItem,
} from "@workspace/ui/components/toggle-group"
import { ORDER_STATUSES, type OrderStatus } from "@/shared/lib/constants"

interface OrderStatusFilterProps {
  value: OrderStatus | null
  onChange: (status: OrderStatus | null) => void
}

export function OrderStatusFilter({
  value,
  onChange,
}: OrderStatusFilterProps) {
  return (
    <ToggleGroup
      type="single"
      value={value ?? "all"}
      onValueChange={(val) => {
        onChange(val === "all" ? null : (val as OrderStatus))
      }}
    >
      <ToggleGroupItem value="all" aria-label="显示全部">
        全部
      </ToggleGroupItem>
      {ORDER_STATUSES.map(({ value: key, label }) => (
        <ToggleGroupItem key={key} value={key} aria-label={label}>
          {label}
        </ToggleGroupItem>
      ))}
    </ToggleGroup>
  )
}
