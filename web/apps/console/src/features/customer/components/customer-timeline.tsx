import {
  Mail,
  Phone,
  MessageSquare,
  Users,
  Paperclip,
} from "lucide-react"
import { Badge } from "@workspace/ui/components/badge"
import { Timeline, type TimelineItem } from "@/shared/components/data/timeline"
import type { FollowUpItem } from "../types"

type CustomerTimelineProps = {
  customerId: string
  followUps: FollowUpItem[]
  className?: string
}

const methodIcons: Record<
  string,
  React.ComponentType<{ className?: string }>
> = {
  email: Mail,
  phone: Phone,
  whatsapp: MessageSquare,
  meeting: Users,
  alibaba: MessageSquare,
  wechat: MessageSquare,
  other: MessageSquare,
}

const methodLabels: Record<string, string> = {
  email: "邮件",
  phone: "电话",
  whatsapp: "WhatsApp",
  meeting: "会面",
  alibaba: "Alibaba",
  wechat: "微信",
  other: "其他",
}

const stageTypeMap: Record<string, TimelineItem["type"]> = {
  quoted: "success",
  ordered: "success",
  lost: "destructive",
  negotiating: "warning",
}

function FollowUpContent({ item }: { item: FollowUpItem }) {
  const label = methodLabels[item.method] ?? item.method

  return (
    <div className="flex flex-col gap-1">
      <div className="flex items-center gap-2">
        <span className="font-medium">{label}</span>
        {item.stage && (
          <Badge variant="secondary" className="text-xs">
            {item.stage}
          </Badge>
        )}
        {item.attachment_count > 0 && (
          <Badge variant="outline" className="gap-1 text-xs">
            <Paperclip className="size-3" />
            {item.attachment_count}
          </Badge>
        )}
      </div>
      <p className="line-clamp-2 text-sm text-muted-foreground">
        {item.content}
      </p>
    </div>
  )
}

export function CustomerTimeline({
  followUps,
  className,
}: CustomerTimelineProps) {
  const timelineItems: TimelineItem[] = followUps.map((item) => ({
    id: item.id,
    time: item.created_at,
    icon: methodIcons[item.method] ?? MessageSquare,
    content: <FollowUpContent item={item} />,
    type: stageTypeMap[item.stage ?? ""] ?? "default",
  }))

  return (
    <Timeline
      items={timelineItems}
      emptyMessage="暂无跟进记录"
      className={className}
    />
  )
}
