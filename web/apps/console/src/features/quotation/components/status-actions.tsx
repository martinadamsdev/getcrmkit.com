import { Button } from "@workspace/ui/components/button"
import { Loader2 } from "lucide-react"
import {
  QUOTATION_STATUS_TRANSITIONS,
  type QuotationStatus,
} from "@/shared/lib/constants"

const TRANSITION_LABELS: Record<QuotationStatus, string> = {
  draft: "标为草稿",
  sent: "标为已发送",
  following: "标为跟进中",
  confirmed: "标为已确认",
  converted: "转为订单",
  expired: "标为已过期",
  rejected: "标为已拒绝",
}

const TRANSITION_VARIANTS: Record<QuotationStatus, "default" | "destructive" | "secondary"> = {
  draft: "secondary",
  sent: "default",
  following: "default",
  confirmed: "default",
  converted: "default",
  expired: "destructive",
  rejected: "destructive",
}

type StatusActionsProps = {
  currentStatus: QuotationStatus
  onTransition: (targetStatus: QuotationStatus) => void
  isLoading: boolean
}

export function StatusActions({
  currentStatus,
  onTransition,
  isLoading,
}: StatusActionsProps) {
  const transitions = QUOTATION_STATUS_TRANSITIONS[currentStatus] ?? []

  if (transitions.length === 0) return null

  return (
    <div className="flex flex-wrap gap-2">
      {transitions.map((target) => (
        <Button
          key={target}
          variant={TRANSITION_VARIANTS[target]}
          onClick={() => onTransition(target)}
          disabled={isLoading}
        >
          {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          {TRANSITION_LABELS[target]}
        </Button>
      ))}
    </div>
  )
}
