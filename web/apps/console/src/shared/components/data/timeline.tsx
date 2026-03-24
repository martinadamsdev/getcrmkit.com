import { formatRelativeTime } from "@/shared/lib/format"
import { Inbox } from "lucide-react"
import { EmptyState } from "./empty-state"

export type TimelineItem = {
  id: string
  time: string | Date
  icon: React.ComponentType<{ className?: string }>
  content: React.ReactNode
  type?: "default" | "success" | "warning" | "destructive"
}

type TimelineProps = {
  items: TimelineItem[]
  emptyMessage?: string
  className?: string
}

const typeColors: Record<string, string> = {
  default: "bg-muted-foreground",
  success: "bg-green-500",
  warning: "bg-amber-500",
  destructive: "bg-red-500",
}

export function Timeline({
  items,
  emptyMessage = "No activity",
  className,
}: TimelineProps) {
  if (items.length === 0) {
    return (
      <EmptyState icon={Inbox} title={emptyMessage} />
    )
  }

  return (
    <div className={`relative space-y-6 ${className ?? ""}`}>
      {items.map((item, index) => {
        const Icon = item.icon
        const colorClass = typeColors[item.type ?? "default"]
        const isLast = index === items.length - 1

        return (
          <div key={item.id} className="relative flex gap-4">
            {/* Connector line */}
            {!isLast && (
              <div className="absolute left-[15px] top-8 bottom-0 w-px bg-border" />
            )}
            {/* Dot */}
            <div
              data-timeline-dot
              className={`relative z-10 flex size-8 shrink-0 items-center justify-center rounded-full ${colorClass}/10`}
            >
              <Icon className={`size-4 ${colorClass.replace("bg-", "text-")}`} />
            </div>
            {/* Content */}
            <div className="flex-1 pt-0.5">
              <div className="text-sm">{item.content}</div>
              <time className="text-xs text-muted-foreground">
                {formatRelativeTime(item.time)}
              </time>
            </div>
          </div>
        )
      })}
    </div>
  )
}
