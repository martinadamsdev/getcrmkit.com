import { renderHook, act } from "@testing-library/react"
import { describe, expect, it, beforeEach } from "vitest"
import { useQuotationProfitCalc } from "../use-quotation-profit-calc"
import { useQuotationEditorStore } from "../../stores/quotation-editor.store"

describe("useQuotationProfitCalc", () => {
  beforeEach(() => {
    act(() => {
      useQuotationEditorStore.getState().reset()
    })
  })

  it("triggers optimistic calculation immediately on change", () => {
    renderHook(() => useQuotationProfitCalc("quotation-123"))

    act(() => {
      useQuotationEditorStore.getState().addItem({
        id: "item-1",
        productId: "p1",
        productName: "Widget",
        material: null,
        quantity: 100,
        costPrice: 10,
        costCurrency: "CNY",
        unitPrice: 2,
        sellingCurrency: "USD",
        multiplier: null,
        subtotal: 200,
        customizationIds: [],
        customizationCost: 0,
        notes: "",
        position: 0,
      })
    })

    const store = useQuotationEditorStore.getState()
    expect(store.optimisticProfit).not.toBeNull()
  })

  it("runs optimistic calc even without quotation id", () => {
    renderHook(() => useQuotationProfitCalc(null))

    act(() => {
      useQuotationEditorStore.getState().addItem({
        id: "item-1",
        productId: "p1",
        productName: "Widget",
        material: null,
        quantity: 100,
        costPrice: 10,
        costCurrency: "CNY",
        unitPrice: 2,
        sellingCurrency: "USD",
        multiplier: null,
        subtotal: 200,
        customizationIds: [],
        customizationCost: 0,
        notes: "",
        position: 0,
      })
    })

    const store = useQuotationEditorStore.getState()
    expect(store.optimisticProfit).not.toBeNull()
    expect(store.optimisticProfit!.totalAmount).toBe(200)
    expect(store.optimisticProfit!.totalCost).toBe(1000)
  })
})
