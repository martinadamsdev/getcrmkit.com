import { Badge } from "@workspace/ui/components/badge"

const defaultColorMap: Record<string, string> = {
  A: "#22c55e", // green
  B: "#3b82f6", // blue
  C: "#f59e0b", // amber
  D: "#9ca3af", // gray/muted
}

type GradeBadgeProps = {
  grade: string
  color?: string
  label?: string
  className?: string
}

export function GradeBadge({
  grade,
  color,
  label,
  className,
}: GradeBadgeProps) {
  const bgColor = color ?? defaultColorMap[grade] ?? "#6b7280"

  return (
    <Badge
      variant="secondary"
      className={className}
      style={{ backgroundColor: bgColor, color: "#fff" }}
    >
      {label ?? grade}
    </Badge>
  )
}
