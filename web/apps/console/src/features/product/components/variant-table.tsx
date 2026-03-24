import { Plus, Trash2 } from "lucide-react"
import { Button } from "@workspace/ui/components/button"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@workspace/ui/components/table"
import { ColorDot } from "@/shared/components/business/color-dot"

interface Variant {
  id: string
  material: string | null
  color: string | null
  color_name: string | null
  size: string | null
  sku: string | null
  cost_price: string | null
}

interface VariantTableProps {
  variants: Variant[]
  onAdd: () => void
  onUpdate: (id: string, field: string, value: string) => void
  onDelete: (id: string) => void
}

export function VariantTable({
  variants,
  onAdd,
  onUpdate,
  onDelete,
}: VariantTableProps) {
  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold">产品变体</h3>
        <Button variant="outline" size="sm" onClick={onAdd}>
          <Plus className="mr-1.5 h-3.5 w-3.5" />
          添加变体
        </Button>
      </div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>材质</TableHead>
            <TableHead>颜色</TableHead>
            <TableHead>尺寸</TableHead>
            <TableHead>SKU</TableHead>
            <TableHead>成本</TableHead>
            <TableHead className="w-[60px]" />
          </TableRow>
        </TableHeader>
        <TableBody>
          {variants.length === 0 ? (
            <TableRow>
              <TableCell
                colSpan={6}
                className="h-16 text-center text-muted-foreground"
              >
                暂无变体，点击"添加变体"创建
              </TableCell>
            </TableRow>
          ) : (
            variants.map((v) => (
              <TableRow key={v.id}>
                <TableCell>
                  <span className="text-sm">{v.material ?? "\u2014"}</span>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    {v.color && (
                      <ColorDot
                        color={v.color}
                        size="sm"
                        label={v.color_name ?? undefined}
                      />
                    )}
                    <span className="text-sm">{v.color_name ?? "\u2014"}</span>
                  </div>
                </TableCell>
                <TableCell>
                  <span className="text-sm">{v.size ?? "\u2014"}</span>
                </TableCell>
                <TableCell>
                  <span className="text-sm font-mono">
                    {v.sku ?? "\u2014"}
                  </span>
                </TableCell>
                <TableCell>
                  <span className="text-sm">
                    {v.cost_price ? `¥${v.cost_price}` : "\u2014"}
                  </span>
                </TableCell>
                <TableCell>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-7 w-7 text-muted-foreground hover:text-destructive"
                    onClick={() => onDelete(v.id)}
                    aria-label="删除"
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                  </Button>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </div>
  )
}
