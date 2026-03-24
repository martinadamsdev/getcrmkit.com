import { Badge } from "@workspace/ui/components/badge"
import { ORDER_STATUS_MAP } from "@/shared/lib/constants"

type BadgeVariant = "default" | "secondary" | "destructive" | "outline"

const VARIANT_MAP: Record<string, BadgeVariant> = {
  default: "default",
  secondary: "secondary",
  destructive: "destructive",
  outline: "outline",
  success: "default",
  warning: "secondary",
  accent: "default",
}

const DOT_COLORS: Record<string, string> = {
  default: "bg-primary",
  secondary: "bg-muted-foreground",
  destructive: "bg-destructive",
  success: "bg-emerald-500",
  warning: "bg-amber-500",
  accent: "bg-blue-500",
}

interface OrderStatusBadgeProps {
  status: string
}

export function OrderStatusBadge({ status }: OrderStatusBadgeProps) {
  const config = ORDER_STATUS_MAP[status as keyof typeof ORDER_STATUS_MAP]
  const label = config?.label ?? status
  const rawVariant = config?.variant ?? "secondary"
  const variant = VARIANT_MAP[rawVariant] ?? "secondary"
  const dotColor = DOT_COLORS[rawVariant] ?? "bg-muted-foreground"

  return (
    <Badge variant={variant}>
      <span
        data-status-dot
        className={`mr-1.5 inline-block size-1.5 rounded-full ${dotColor}`}
      />
      {label}
    </Badge>
  )
}
