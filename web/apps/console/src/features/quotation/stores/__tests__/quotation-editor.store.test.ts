import { act, renderHook } from "@testing-library/react"
import { afterEach, describe, expect, it } from "vitest"
import {
  useQuotationEditorStore,
  type QuotationLineItem,
} from "../quotation-editor.store"

const makeItem = (overrides: Partial<QuotationLineItem> = {}): QuotationLineItem => ({
  id: crypto.randomUUID(),
  productId: crypto.randomUUID(),
  productName: "Test Widget",
  material: "ABS",
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
  ...overrides,
})

describe("quotation-editor store", () => {
  afterEach(() => {
    act(() => {
      useQuotationEditorStore.getState().reset()
    })
  })

  it("initializes with empty state", () => {
    const { result } = renderHook(() => useQuotationEditorStore())
    expect(result.current.items).toEqual([])
    expect(result.current.tradeTerm).toBe("FOB")
    expect(result.current.currency).toBe("USD")
    expect(result.current.freight).toBe(0)
    expect(result.current.insurance).toBe(0)
    expect(result.current.otherCost).toBe(0)
    expect(result.current.isDirty).toBe(false)
  })

  it("adds a line item", () => {
    const { result } = renderHook(() => useQuotationEditorStore())
    const item = makeItem()
    act(() => {
      result.current.addItem(item)
    })
    expect(result.current.items).toHaveLength(1)
    expect(result.current.items[0].productName).toBe("Test Widget")
    expect(result.current.isDirty).toBe(true)
  })

  it("removes a line item", () => {
    const { result } = renderHook(() => useQuotationEditorStore())
    const item = makeItem()
    act(() => {
      result.current.addItem(item)
      result.current.removeItem(item.id)
    })
    expect(result.current.items).toHaveLength(0)
  })

  it("updates a line item field", () => {
    const { result } = renderHook(() => useQuotationEditorStore())
    const item = makeItem()
    act(() => {
      result.current.addItem(item)
      result.current.updateItem(item.id, { quantity: 250, subtotal: 500 })
    })
    expect(result.current.items[0].quantity).toBe(250)
    expect(result.current.items[0].subtotal).toBe(500)
  })

  it("calculates optimistic profit", () => {
    const { result } = renderHook(() => useQuotationEditorStore())
    const item = makeItem({
      quantity: 100,
      costPrice: 10,
      unitPrice: 2,
      subtotal: 200,
    })
    act(() => {
      result.current.addItem(item)
      result.current.recalculateOptimistic()
    })
    const profit = result.current.optimisticProfit
    expect(profit).not.toBeNull()
    expect(profit!.totalAmount).toBe(200)
    expect(profit!.totalCost).toBe(1000)
  })

  it("sets freight and insurance", () => {
    const { result } = renderHook(() => useQuotationEditorStore())
    act(() => {
      result.current.setFreight(200)
      result.current.setInsurance(50)
    })
    expect(result.current.freight).toBe(200)
    expect(result.current.insurance).toBe(50)
    expect(result.current.isDirty).toBe(true)
  })

  it("applies server profit result overwriting optimistic", () => {
    const { result } = renderHook(() => useQuotationEditorStore())
    const serverResult = {
      totalAmount: 1680,
      totalCost: 12000,
      totalProfit: 480,
      profitRate: 0.286,
      freight: 200,
      insurance: 50,
      grandTotal: 1930,
    }
    act(() => {
      result.current.applyServerProfit(serverResult)
    })
    expect(result.current.serverProfit).toEqual(serverResult)
  })

  it("resets to initial state", () => {
    const { result } = renderHook(() => useQuotationEditorStore())
    act(() => {
      result.current.addItem(makeItem())
      result.current.setFreight(100)
      result.current.reset()
    })
    expect(result.current.items).toEqual([])
    expect(result.current.freight).toBe(0)
    expect(result.current.isDirty).toBe(false)
  })

  it("loads existing quotation into store", () => {
    const { result } = renderHook(() => useQuotationEditorStore())
    const items = [makeItem(), makeItem({ productName: "Another" })]
    act(() => {
      result.current.loadQuotation({
        items,
        tradeTerm: "CIF",
        currency: "EUR",
        freight: 300,
        insurance: 80,
        otherCost: 20,
        exchangeRate: 7.85,
      })
    })
    expect(result.current.items).toHaveLength(2)
    expect(result.current.tradeTerm).toBe("CIF")
    expect(result.current.currency).toBe("EUR")
    expect(result.current.freight).toBe(300)
    expect(result.current.isDirty).toBe(false)
  })

  it("sets trade term", () => {
    const { result } = renderHook(() => useQuotationEditorStore())
    act(() => {
      result.current.setTradeTerm("CIF")
    })
    expect(result.current.tradeTerm).toBe("CIF")
  })

  it("sets currency", () => {
    const { result } = renderHook(() => useQuotationEditorStore())
    act(() => {
      result.current.setCurrency("EUR")
    })
    expect(result.current.currency).toBe("EUR")
  })

  it("sets exchange rate", () => {
    const { result } = renderHook(() => useQuotationEditorStore())
    act(() => {
      result.current.setExchangeRate(7.85)
    })
    expect(result.current.exchangeRate).toBe(7.85)
  })
})
