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

interface PricingTier {
  id: string
  min_qty: number
  max_qty: number | null
  multiplier: string
}

interface PricingTierTableProps {
  tiers: PricingTier[]
  onAdd: () => void
  onUpdate: (id: string, field: string, value: string) => void
  onDelete: (id: string) => void
}

export function PricingTierTable({
  tiers,
  onAdd,
  onUpdate,
  onDelete,
}: PricingTierTableProps) {
  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold">阶梯定价</h3>
        <Button variant="outline" size="sm" onClick={onAdd}>
          <Plus className="mr-1.5 h-3.5 w-3.5" />
          添加阶梯
        </Button>
      </div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>最小数量</TableHead>
            <TableHead>最大数量</TableHead>
            <TableHead>倍率</TableHead>
            <TableHead className="w-[60px]" />
          </TableRow>
        </TableHeader>
        <TableBody>
          {tiers.length === 0 ? (
            <TableRow>
              <TableCell
                colSpan={4}
                className="h-16 text-center text-muted-foreground"
              >
                暂无阶梯定价
              </TableCell>
            </TableRow>
          ) : (
            tiers.map((tier) => (
              <TableRow key={tier.id}>
                <TableCell>
                  <input
                    type="number"
                    className="h-8 w-24 rounded border border-input bg-transparent px-2 text-sm"
                    value={tier.min_qty}
                    onChange={(e) =>
                      onUpdate(tier.id, "min_qty", e.target.value)
                    }
                    min="0"
                  />
                </TableCell>
                <TableCell>
                  <input
                    type="number"
                    className="h-8 w-24 rounded border border-input bg-transparent px-2 text-sm"
                    value={tier.max_qty ?? ""}
                    onChange={(e) =>
                      onUpdate(tier.id, "max_qty", e.target.value)
                    }
                    placeholder="不限"
                    min="0"
                  />
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-1">
                    <input
                      type="number"
                      className="h-8 w-20 rounded border border-input bg-transparent px-2 text-sm"
                      value={tier.multiplier}
                      onChange={(e) =>
                        onUpdate(tier.id, "multiplier", e.target.value)
                      }
                      step="0.01"
                      min="0"
                    />
                    <span className="text-sm text-muted-foreground">
                      &times;
                    </span>
                  </div>
                </TableCell>
                <TableCell>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-7 w-7 text-muted-foreground hover:text-destructive"
                    onClick={() => onDelete(tier.id)}
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
