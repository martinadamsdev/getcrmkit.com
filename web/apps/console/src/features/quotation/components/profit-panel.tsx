import { Loader2 } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@workspace/ui/components/card"
import { Separator } from "@workspace/ui/components/separator"
import { cn } from "@workspace/ui/lib/utils"
import { formatMoney } from "@/shared/lib/format"
import { useQuotationEditorStore } from "../stores/quotation-editor.store"

export function ProfitPanel() {
  const { optimisticProfit, serverProfit, isCalculating, currency, items } =
    useQuotationEditorStore()

  const profit = serverProfit ?? optimisticProfit

  if (!profit) {
    return (
      <Card className="sticky top-4">
        <CardHeader>
          <CardTitle className="text-base">利润面板</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            添加产品后显示利润计算结果
          </p>
        </CardContent>
      </Card>
    )
  }

  const profitSign =
    profit.profitRate > 0
      ? "positive"
      : profit.profitRate < 0
        ? "negative"
        : "zero"

  return (
    <Card className="sticky top-4">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-base">利润面板</CardTitle>
        {isCalculating && (
          <span className="flex items-center gap-1 text-xs text-muted-foreground">
            <Loader2 className="h-3 w-3 animate-spin" />
            计算中...
          </span>
        )}
      </CardHeader>
      <CardContent className="space-y-3">
        <ProfitRow label="成本">
          <span className="tabular-nums">
            {formatMoney(profit.totalCost, "CNY")}
          </span>
        </ProfitRow>
        <ProfitRow label="售价">
          <span className="tabular-nums">
            {formatMoney(profit.totalAmount, currency)}
          </span>
        </ProfitRow>
        <ProfitRow label="利润">
          <span className="tabular-nums">
            {formatMoney(profit.totalProfit, currency)}
          </span>
        </ProfitRow>
        <ProfitRow label="利润率">
          <span
            data-profit={profitSign}
            className={cn(
              "font-semibold tabular-nums",
              profitSign === "positive" && "text-green-600",
              profitSign === "negative" && "text-destructive",
            )}
          >
            {(profit.profitRate * 100).toFixed(1)}%
          </span>
        </ProfitRow>
        <Separator />
        <ProfitRow label="运费">
          <span className="tabular-nums">
            {formatMoney(profit.freight, currency)}
          </span>
        </ProfitRow>
        <ProfitRow label="保险">
          <span className="tabular-nums">
            {formatMoney(profit.insurance, currency)}
          </span>
        </ProfitRow>
        <Separator />
        <ProfitRow label="合计" bold>
          <span className="font-bold text-lg tabular-nums">
            {formatMoney(profit.grandTotal, currency)}
          </span>
        </ProfitRow>

        {/* Per-item breakdown */}
        {items.length > 0 && (
          <>
            <Separator />
            <p className="text-xs font-medium text-muted-foreground pt-1">
              明细
            </p>
            {items.map((item) => {
              const itemCost = item.costPrice * item.quantity + item.customizationCost
              const itemProfit = item.subtotal - itemCost
              return (
                <div key={item.id} className="flex items-center justify-between text-xs">
                  <span className="truncate max-w-[140px]" title={item.productName}>
                    {item.productName}
                  </span>
                  <span
                    className={cn(
                      "tabular-nums",
                      itemProfit > 0 && "text-green-600",
                      itemProfit < 0 && "text-destructive",
                    )}
                  >
                    {formatMoney(itemProfit, currency)}
                  </span>
                </div>
              )
            })}
          </>
        )}
      </CardContent>
    </Card>
  )
}

function ProfitRow({
  label,
  children,
  bold = false,
}: {
  label: string
  children: React.ReactNode
  bold?: boolean
}) {
  return (
    <div className="flex items-center justify-between">
      <span
        className={cn(
          "text-sm text-muted-foreground",
          bold && "font-semibold text-foreground",
        )}
      >
        {label}
      </span>
      {children}
    </div>
  )
}
