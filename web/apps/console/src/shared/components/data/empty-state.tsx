import { Button } from "@workspace/ui/components/button"

type EmptyStateProps = {
  icon: React.ComponentType<{ className?: string }>
  title: string
  description?: string
  action?: { label: string; onClick: () => void }
  className?: string
}

export function EmptyState({
  icon: Icon,
  title,
  description,
  action,
  className,
}: EmptyStateProps) {
  return (
    <div
      className={`flex flex-col items-center justify-center gap-3 py-12 ${className ?? ""}`}
    >
      <Icon className="size-12 text-muted-foreground" />
      <h3 className="text-lg font-medium">{title}</h3>
      {description && (
        <p className="max-w-sm text-center text-sm text-muted-foreground">
          {description}
        </p>
      )}
      {action && (
        <Button onClick={action.onClick} className="mt-2">
          {action.label}
        </Button>
      )}
    </div>
  )
}
