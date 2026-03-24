import { Badge } from "@workspace/ui/components/badge"

type BadgeVariant = "default" | "secondary" | "destructive" | "outline"

const defaultColorMap: Record<string, BadgeVariant> = {
  new: "secondary",
  contacted: "default",
  quoted: "default",
  sample_sent: "default",
  negotiating: "default",
  ordered: "default",
  lost: "destructive",
  active: "default",
  inactive: "secondary",
}

const dotColors: Record<BadgeVariant, string> = {
  default: "bg-primary",
  secondary: "bg-muted-foreground",
  destructive: "bg-destructive",
  outline: "bg-foreground",
}

type StatusBadgeProps = {
  status: string
  colorMap?: Record<string, BadgeVariant>
  labelMap?: Record<string, string>
  className?: string
}

export function StatusBadge({
  status,
  colorMap,
  labelMap,
  className,
}: StatusBadgeProps) {
  const effectiveColorMap = { ...defaultColorMap, ...colorMap }
  const variant = effectiveColorMap[status] ?? "secondary"
  const label = labelMap?.[status] ?? status

  return (
    <Badge variant={variant} className={className}>
      <span
        data-status-dot
        className={`mr-1.5 inline-block size-1.5 rounded-full ${dotColors[variant]}`}
      />
      {label}
    </Badge>
  )
}
