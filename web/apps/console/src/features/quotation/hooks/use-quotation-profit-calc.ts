import { useEffect, useRef } from "react"
import { useQuotationEditorStore } from "../stores/quotation-editor.store"

const DEBOUNCE_MS = 300

export function useQuotationProfitCalc(quotationId: string | null) {
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const { items, freight, insurance, otherCost, exchangeRate, currency } =
    useQuotationEditorStore()
  const { recalculateOptimistic, applyServerProfit, setIsCalculating } =
    useQuotationEditorStore()

  useEffect(() => {
    recalculateOptimistic()

    if (!quotationId || items.length === 0) {
      setIsCalculating(false)
      return
    }

    if (timerRef.current) clearTimeout(timerRef.current)
    setIsCalculating(true)

    let cancelled = false

    timerRef.current = setTimeout(async () => {
      try {
        const res = await fetch(
          `/api/v1/quotations/${quotationId}/calculate-profit`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              items: items.map((i) => ({
                product_id: i.productId,
                quantity: i.quantity,
                cost_price: i.costPrice,
                cost_currency: i.costCurrency,
                unit_price: i.unitPrice,
                selling_currency: i.sellingCurrency,
                customization_cost: i.customizationCost,
              })),
              freight,
              insurance,
              other_cost: otherCost,
              exchange_rate: exchangeRate,
              currency,
            }),
          },
        )

        if (cancelled) return
        if (!res.ok) throw new Error("Profit calculation failed")

        const data = await res.json()
        if (cancelled) return
        applyServerProfit({
          totalAmount: data.total_amount,
          totalCost: data.total_cost,
          totalProfit: data.total_profit,
          profitRate: data.profit_rate,
          freight: data.freight,
          insurance: data.insurance,
          grandTotal: data.grand_total,
        })
      } catch {
        if (!cancelled) setIsCalculating(false)
      }
    }, DEBOUNCE_MS)

    return () => {
      cancelled = true
      if (timerRef.current) clearTimeout(timerRef.current)
      setIsCalculating(false)
    }
  }, [items, freight, insurance, otherCost, exchangeRate, currency, quotationId])
}
