import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { act } from "@testing-library/react"
import { afterEach, describe, expect, it } from "vitest"
import { QuotationItemTable } from "../quotation-item-table"
import { useQuotationEditorStore } from "../../stores/quotation-editor.store"

describe("QuotationItemTable", () => {
  afterEach(() => {
    act(() => {
      useQuotationEditorStore.getState().reset()
    })
  })

  it("renders add button when no items", () => {
    render(<QuotationItemTable />)
    expect(screen.getByText("添加产品")).toBeInTheDocument()
  })

  it("renders line items from store", () => {
    act(() => {
      useQuotationEditorStore.getState().addItem({
        id: "item-1",
        productId: "p1",
        productName: "Widget A",
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
      })
    })

    render(<QuotationItemTable />)
    expect(screen.getByText("Widget A")).toBeInTheDocument()
    expect(screen.getByDisplayValue("100")).toBeInTheDocument()
    expect(screen.getByDisplayValue("2")).toBeInTheDocument()
  })

  it("shows table headers", () => {
    render(<QuotationItemTable />)
    expect(screen.getByText("产品")).toBeInTheDocument()
    expect(screen.getByText("数量")).toBeInTheDocument()
    expect(screen.getByText("单价")).toBeInTheDocument()
    expect(screen.getByText("小计")).toBeInTheDocument()
  })

  it("deletes a line item when delete button clicked", async () => {
    const user = userEvent.setup()
    act(() => {
      useQuotationEditorStore.getState().addItem({
        id: "item-1",
        productId: "p1",
        productName: "Widget A",
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

    render(<QuotationItemTable />)
    const deleteBtn = screen.getByRole("button", { name: /删除/ })
    await user.click(deleteBtn)
    expect(useQuotationEditorStore.getState().items).toHaveLength(0)
  })

  it("updates quantity and recalculates subtotal", async () => {
    const user = userEvent.setup()
    act(() => {
      useQuotationEditorStore.getState().addItem({
        id: "item-1",
        productId: "p1",
        productName: "Widget A",
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

    render(<QuotationItemTable />)
    const qtyInput = screen.getByDisplayValue("100")
    await user.clear(qtyInput)
    await user.type(qtyInput, "250")
    const updated = useQuotationEditorStore.getState().items[0]
    expect(updated.quantity).toBe(250)
    expect(updated.subtotal).toBe(500)
  })
})
