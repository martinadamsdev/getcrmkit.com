import { cn } from "@workspace/ui/lib/utils"

const SIZE_MAP = {
  sm: "h-3 w-3",
  md: "h-4 w-4",
  lg: "h-5 w-5",
} as const

interface ColorDotProps {
  color: string
  size?: "sm" | "md" | "lg"
  label?: string
  className?: string
}

export function ColorDot({
  color,
  size = "md",
  label,
  className,
}: ColorDotProps) {
  return (
    <span
      className={cn(
        "inline-block rounded-full border border-border/50 shrink-0",
        SIZE_MAP[size],
        className,
      )}
      style={{ backgroundColor: color }}
      {...(label
        ? { role: "img" as const, "aria-label": label }
        : { "aria-hidden": true as const })}
    />
  )
}
