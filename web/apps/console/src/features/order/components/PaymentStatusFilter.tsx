import {
  ToggleGroup,
  ToggleGroupItem,
} from "@workspace/ui/components/toggle-group"
import { PAYMENT_STATUSES, type PaymentStatus } from "@/shared/lib/constants"

interface PaymentStatusFilterProps {
  value: PaymentStatus | null
  onChange: (status: PaymentStatus | null) => void
}

export function PaymentStatusFilter({
  value,
  onChange,
}: PaymentStatusFilterProps) {
  return (
    <ToggleGroup
      type="single"
      value={value ?? "all"}
      onValueChange={(val) => {
        onChange(val === "all" ? null : (val as PaymentStatus))
      }}
    >
      <ToggleGroupItem value="all" aria-label="显示全部付款状态">
        全部
      </ToggleGroupItem>
      {PAYMENT_STATUSES.map(({ value: key, label }) => (
        <ToggleGroupItem key={key} value={key} aria-label={label}>
          {label}
        </ToggleGroupItem>
      ))}
    </ToggleGroup>
  )
}
