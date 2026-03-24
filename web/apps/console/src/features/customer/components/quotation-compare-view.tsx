import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@workspace/ui/components/table"
import { formatMoney } from "@/shared/lib/format"
import type { QuotationDetail } from "../types"

type QuotationCompareViewProps = {
  quotationA: QuotationDetail
  quotationB: QuotationDetail
  className?: string
}

function getDiffClass(a: number, b: number): string {
  if (b > a) return "bg-green-50 text-green-700 dark:bg-green-950 dark:text-green-300"
  if (b < a) return "bg-red-50 text-red-700 dark:bg-red-950 dark:text-red-300"
  return ""
}

function getTextDiffClass(a: string | null | undefined, b: string | null | undefined): string {
  if (a !== b) return "bg-amber-50 text-amber-700 dark:bg-amber-950 dark:text-amber-300"
  return ""
}

export function QuotationCompareView({
  quotationA,
  quotationB,
  className,
}: QuotationCompareViewProps) {
  // Build a union of all line items by product name
  const allProductNames = new Set([
    ...quotationA.line_items.map((i) => i.product_name),
    ...quotationB.line_items.map((i) => i.product_name),
  ])

  const itemMapA = new Map(
    quotationA.line_items.map((i) => [i.product_name, i]),
  )
  const itemMapB = new Map(
    quotationB.line_items.map((i) => [i.product_name, i]),
  )

  return (
    <div className={className}>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-32">比较项</TableHead>
            <TableHead>{quotationA.quotation_no}</TableHead>
            <TableHead>{quotationB.quotation_no}</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {/* Summary rows */}
          <TableRow>
            <TableCell className="font-medium">客户</TableCell>
            <TableCell>{quotationA.customer_name}</TableCell>
            <TableCell>{quotationB.customer_name}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell className="font-medium">总金额</TableCell>
            <TableCell>
              {formatMoney(quotationA.total_amount, quotationA.currency)}
            </TableCell>
            <TableCell
              className={getDiffClass(
                quotationA.total_amount,
                quotationB.total_amount,
              )}
            >
              {formatMoney(quotationB.total_amount, quotationB.currency)}
            </TableCell>
          </TableRow>
          <TableRow>
            <TableCell className="font-medium">贸易条款</TableCell>
            <TableCell>{quotationA.trade_terms ?? "—"}</TableCell>
            <TableCell
              className={getTextDiffClass(
                quotationA.trade_terms,
                quotationB.trade_terms,
              )}
            >
              {quotationB.trade_terms ?? "—"}
            </TableCell>
          </TableRow>
          <TableRow>
            <TableCell className="font-medium">币种</TableCell>
            <TableCell>{quotationA.currency}</TableCell>
            <TableCell
              className={getTextDiffClass(
                quotationA.currency,
                quotationB.currency,
              )}
            >
              {quotationB.currency}
            </TableCell>
          </TableRow>

          {/* Line items */}
          {[...allProductNames].map((productName) => {
            const itemA = itemMapA.get(productName)
            const itemB = itemMapB.get(productName)

            return (
              <TableRow key={productName}>
                <TableCell className="font-medium">{productName}</TableCell>
                <TableCell>
                  {itemA ? (
                    <span>
                      {itemA.quantity} x{" "}
                      {formatMoney(itemA.unit_price, quotationA.currency)}
                    </span>
                  ) : (
                    <span className="text-muted-foreground">—</span>
                  )}
                </TableCell>
                <TableCell
                  className={
                    itemA && itemB
                      ? getDiffClass(itemA.unit_price, itemB.unit_price)
                      : itemB
                        ? "bg-green-50 text-green-700 dark:bg-green-950 dark:text-green-300"
                        : ""
                  }
                >
                  {itemB ? (
                    <span>
                      {itemB.quantity} x{" "}
                      {formatMoney(itemB.unit_price, quotationB.currency)}
                    </span>
                  ) : (
                    <span className="text-muted-foreground">—</span>
                  )}
                </TableCell>
              </TableRow>
            )
          })}
        </TableBody>
      </Table>
    </div>
  )
}
