import { useState } from "react"
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  type DragEndEvent,
} from "@dnd-kit/core"
import {
  SortableContext,
  sortableKeyboardCoordinates,
  useSortable,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable"
import { CSS } from "@dnd-kit/utilities"
import { ChevronRight, Folder, GripVertical } from "lucide-react"
import { cn } from "@workspace/ui/lib/utils"
import { Badge } from "@workspace/ui/components/badge"

interface CategoryNode {
  id: string
  name: string
  parent_id: string | null
  level: number
  position: number
  product_count: number
  children: CategoryNode[]
}

interface CategoryTreeProps {
  categories: CategoryNode[]
  selectedId: string | null
  onSelect: (id: string) => void
  onReorder: (items: { id: string; position: number }[]) => void
}

interface CategoryItemProps {
  node: CategoryNode
  selectedId: string | null
  onSelect: (id: string) => void
  depth: number
}

function SortableCategoryItem({
  node,
  selectedId,
  onSelect,
  depth,
}: CategoryItemProps) {
  const [expanded, setExpanded] = useState(false)
  const hasChildren = node.children.length > 0
  const isSelected = node.id === selectedId

  const { attributes, listeners, setNodeRef, transform, transition, isDragging } =
    useSortable({ id: node.id })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  }

  return (
    <div ref={setNodeRef} style={style}>
      <div
        data-selected={isSelected}
        className={cn(
          "flex items-center gap-1 rounded-md px-2 py-1.5 text-sm cursor-pointer hover:bg-accent/50 transition-colors",
          isSelected && "bg-accent text-accent-foreground",
          isDragging && "opacity-50",
        )}
        style={{ paddingLeft: `${depth * 16 + 8}px` }}
        onClick={() => {
          onSelect(node.id)
          if (hasChildren) setExpanded(!expanded)
        }}
      >
        <button
          type="button"
          className="cursor-grab touch-none p-0.5"
          {...attributes}
          {...listeners}
        >
          <GripVertical className="h-3.5 w-3.5 text-muted-foreground/50" />
        </button>

        {hasChildren ? (
          <ChevronRight
            className={cn(
              "h-3.5 w-3.5 shrink-0 transition-transform",
              expanded && "rotate-90",
            )}
          />
        ) : (
          <span className="w-3.5" />
        )}

        <Folder className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
        <span className="flex-1 truncate">{node.name}</span>
        <Badge
          variant="secondary"
          className="text-[10px] h-4 min-w-[20px] justify-center"
        >
          {node.product_count}
        </Badge>
      </div>

      {expanded && hasChildren && (
        <div>
          {node.children.map((child) => (
            <SortableCategoryItem
              key={child.id}
              node={child}
              selectedId={selectedId}
              onSelect={onSelect}
              depth={depth + 1}
            />
          ))}
        </div>
      )}
    </div>
  )
}

export function CategoryTree({
  categories,
  selectedId,
  onSelect,
  onReorder,
}: CategoryTreeProps) {
  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 8 } }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    }),
  )

  // NOTE: v1.0.0 only supports top-level category reorder.
  // Nested category reorder requires per-level SortableContext (v2.0.0+)
  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event
    if (!over || active.id === over.id) return

    const flatIds = categories.map((c) => c.id)
    const oldIndex = flatIds.indexOf(String(active.id))
    const newIndex = flatIds.indexOf(String(over.id))
    if (oldIndex === -1 || newIndex === -1) return

    const reordered = [...flatIds]
    reordered.splice(oldIndex, 1)
    reordered.splice(newIndex, 0, String(active.id))

    onReorder(reordered.map((id, idx) => ({ id, position: idx })))
  }

  if (categories.length === 0) {
    return (
      <div className="flex items-center justify-center py-8 text-sm text-muted-foreground">
        暂无分类
      </div>
    )
  }

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragEnd={handleDragEnd}
    >
      <SortableContext
        items={categories.map((c) => c.id)}
        strategy={verticalListSortingStrategy}
      >
        <div className="space-y-0.5">
          {categories.map((cat) => (
            <SortableCategoryItem
              key={cat.id}
              node={cat}
              selectedId={selectedId}
              onSelect={onSelect}
              depth={0}
            />
          ))}
        </div>
      </SortableContext>
    </DndContext>
  )
}
