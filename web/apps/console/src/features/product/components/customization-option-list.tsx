import { Plus, Trash2 } from "lucide-react"
import { Button } from "@workspace/ui/components/button"

interface CustomizationOption {
  id: string
  name: string
  surcharge: string
}

interface CustomizationOptionListProps {
  options: CustomizationOption[]
  onAdd: () => void
  onUpdate: (id: string, field: string, value: string) => void
  onDelete: (id: string) => void
}

export function CustomizationOptionList({
  options,
  onAdd,
  onUpdate,
  onDelete,
}: CustomizationOptionListProps) {
  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold">定制选项</h3>
        <Button variant="outline" size="sm" onClick={onAdd}>
          <Plus className="mr-1.5 h-3.5 w-3.5" />
          添加选项
        </Button>
      </div>

      {options.length === 0 ? (
        <p className="text-sm text-muted-foreground text-center py-4">
          暂无定制选项
        </p>
      ) : (
        <div className="space-y-2">
          {options.map((opt) => (
            <div
              key={opt.id}
              className="flex items-center gap-3 rounded-md border p-2"
            >
              <input
                className="h-8 flex-1 rounded border border-input bg-transparent px-2 text-sm"
                value={opt.name}
                onChange={(e) => onUpdate(opt.id, "name", e.target.value)}
                placeholder="选项名称"
              />
              <div className="flex items-center gap-1">
                <span className="text-sm text-muted-foreground">+&yen;</span>
                <input
                  type="number"
                  className="h-8 w-20 rounded border border-input bg-transparent px-2 text-sm"
                  value={opt.surcharge}
                  onChange={(e) =>
                    onUpdate(opt.id, "surcharge", e.target.value)
                  }
                  placeholder="0.00"
                  step="0.01"
                  min="0"
                />
              </div>
              <Button
                variant="ghost"
                size="icon"
                className="h-7 w-7 text-muted-foreground hover:text-destructive shrink-0"
                onClick={() => onDelete(opt.id)}
                aria-label="删除"
              >
                <Trash2 className="h-3.5 w-3.5" />
              </Button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
