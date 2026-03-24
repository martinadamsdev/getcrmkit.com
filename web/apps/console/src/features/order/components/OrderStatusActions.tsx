import { Button } from "@workspace/ui/components/button"
import { Loader2 } from "lucide-react"
import {
  ORDER_STATUS_TRANSITIONS,
  ORDER_CANCELLABLE_STATUSES,
  type OrderStatus,
} from "@/shared/lib/constants"

const TRANSITION_LABELS: Partial<Record<OrderStatus, string>> = {
  confirmed: "确认订单",
  producing: "开始生产",
  ready_to_ship: "标记待发",
  shipping: "标记发货",
  delivered: "标记送达",
  completed: "标记完成",
  cancelled: "取消订单",
}

interface OrderStatusActionsProps {
  currentStatus: OrderStatus
  onTransition: (targetStatus: OrderStatus) => void
  isLoading: boolean
}

export function OrderStatusActions({
  currentStatus,
  onTransition,
  isLoading,
}: OrderStatusActionsProps) {
  const transitions = ORDER_STATUS_TRANSITIONS[currentStatus] ?? []

  if (transitions.length === 0) return null

  const forwardTransitions = transitions.filter((t) => t !== "cancelled")
  const canCancel = ORDER_CANCELLABLE_STATUSES.includes(currentStatus)

  return (
    <div className="flex flex-wrap gap-2">
      {forwardTransitions.map((target) => (
        <Button
          key={target}
          variant="default"
          onClick={() => onTransition(target)}
          disabled={isLoading}
        >
          {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          {TRANSITION_LABELS[target]}
        </Button>
      ))}
      {canCancel && (
        <Button
          variant="destructive"
          onClick={() => onTransition("cancelled")}
          disabled={isLoading}
        >
          {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          取消订单
        </Button>
      )}
    </div>
  )
}
