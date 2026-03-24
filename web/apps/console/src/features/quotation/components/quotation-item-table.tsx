import { useCallback } from "react"
import { Plus, Trash2 } from "lucide-react"
import { Button } from "@workspace/ui/components/button"
import { Input } from "@workspace/ui/components/input"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@workspace/ui/components/table"
import { formatMoney } from "@/shared/lib/format"
import { useQuotationEditorStore } from "../stores/quotation-editor.store"

export function QuotationItemTable() {
  const { items, updateItem, removeItem, currency } =
    useQuotationEditorStore()

  const handleQuantityChange = useCallback(
    (itemId: string, qty: number, unitPrice: number) => {
      updateItem(itemId, {
        quantity: qty,
        subtotal: qty * unitPrice,
      })
    },
    [updateItem],
  )

  const handleUnitPriceChange = useCallback(
    (itemId: string, price: number, quantity: number) => {
      updateItem(itemId, {
        unitPrice: price,
        subtotal: quantity * price,
      })
    },
    [updateItem],
  )

  return (
    <div className="space-y-3">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[240px]">产品</TableHead>
            <TableHead className="w-[100px]">规格</TableHead>
            <TableHead className="w-[100px]">数量</TableHead>
            <TableHead className="w-[80px]">单位</TableHead>
            <TableHead className="w-[120px]">单价</TableHead>
            <TableHead className="w-[120px]">小计</TableHead>
            <TableHead className="w-[60px]" />
          </TableRow>
        </TableHeader>
        <TableBody>
          {items.map((item) => (
            <TableRow key={item.id}>
              <TableCell>
                <span className="font-medium">{item.productName}</span>
              </TableCell>
              <TableCell>
                {item.material ? (
                  <span className="text-sm text-muted-foreground">
                    {item.material}
                  </span>
                ) : (
                  <span className="text-muted-foreground">—</span>
                )}
              </TableCell>
              <TableCell>
                <Input
                  type="number"
                  value={item.quantity}
                  onChange={(e) =>
                    handleQuantityChange(
                      item.id,
                      Number(e.target.value),
                      item.unitPrice,
                    )
                  }
                  min={1}
                  className="w-20"
                />
              </TableCell>
              <TableCell>
                <span className="text-sm text-muted-foreground">
                  {item.sellingCurrency}
                </span>
              </TableCell>
              <TableCell>
                <Input
                  type="number"
                  value={item.unitPrice}
                  onChange={(e) =>
                    handleUnitPriceChange(
                      item.id,
                      Number(e.target.value),
                      item.quantity,
                    )
                  }
                  min={0}
                  step={0.01}
                  className="w-24"
                />
              </TableCell>
              <TableCell>
                <span className="tabular-nums">
                  {formatMoney(item.subtotal, currency)}
                </span>
              </TableCell>
              <TableCell>
                <Button
                  variant="ghost"
                  size="icon"
                  aria-label="删除"
                  onClick={() => removeItem(item.id)}
                >
                  <Trash2 className="h-4 w-4 text-muted-foreground" />
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Button variant="outline" className="w-full">
        <Plus className="mr-2 h-4 w-4" />
        添加产品
      </Button>
    </div>
  )
}
