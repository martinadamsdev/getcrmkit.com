import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import { CustomerQuotations } from "./customer-quotations"
import type { QuotationDetail, QuotationSummary } from "../types"

const mockQuotations: QuotationSummary[] = [
  {
    id: "q-1",
    quotation_no: "QT-2026-001",
    customer_id: "cust-1",
    total_amount: 15000,
    currency: "USD",
    trade_terms: "FOB",
    status: "sent",
    created_at: "2026-01-15T00:00:00Z",
  },
  {
    id: "q-2",
    quotation_no: "QT-2026-002",
    customer_id: "cust-1",
    total_amount: 18000,
    currency: "USD",
    trade_terms: "CIF",
    status: "confirmed",
    created_at: "2026-02-01T00:00:00Z",
  },
  {
    id: "q-3",
    quotation_no: "QT-2026-003",
    customer_id: "cust-1",
    total_amount: 12000,
    currency: "USD",
    trade_terms: "FOB",
    status: "draft",
    created_at: "2026-03-01T00:00:00Z",
  },
]

const mockDetailA: QuotationDetail = {
  id: "q-1",
  quotation_no: "QT-2026-001",
  customer_name: "Acme Corp",
  total_amount: 15000,
  currency: "USD",
  trade_terms: "FOB",
  status: "sent",
  line_items: [
    { id: "li-1", product_name: "LED Light A", quantity: 100, unit_price: 100, amount: 10000 },
    { id: "li-2", product_name: "LED Light B", quantity: 50, unit_price: 100, amount: 5000 },
  ],
  created_at: "2026-01-15T00:00:00Z",
}

const mockDetailB: QuotationDetail = {
  id: "q-2",
  quotation_no: "QT-2026-002",
  customer_name: "Acme Corp",
  total_amount: 18000,
  currency: "USD",
  trade_terms: "CIF",
  status: "confirmed",
  line_items: [
    { id: "li-3", product_name: "LED Light A", quantity: 100, unit_price: 120, amount: 12000 },
    { id: "li-4", product_name: "LED Light B", quantity: 50, unit_price: 120, amount: 6000 },
  ],
  created_at: "2026-02-01T00:00:00Z",
}

describe("CustomerQuotations", () => {
  it("renders quotation list with columns: 报价编号, 金额, 贸易条款, 状态, 日期", () => {
    render(<CustomerQuotations quotations={mockQuotations} />)

    expect(screen.getByText("报价编号")).toBeInTheDocument()
    expect(screen.getByText("金额")).toBeInTheDocument()
    expect(screen.getByText("贸易条款")).toBeInTheDocument()
    expect(screen.getByText("状态")).toBeInTheDocument()
    expect(screen.getByText("日期")).toBeInTheDocument()

    expect(screen.getByText("QT-2026-001")).toBeInTheDocument()
    expect(screen.getByText("QT-2026-002")).toBeInTheDocument()
  })

  it("checkbox column allows selecting rows (max 2)", async () => {
    const user = userEvent.setup()
    render(<CustomerQuotations quotations={mockQuotations} />)

    const checkboxes = screen.getAllByRole("checkbox")
    expect(checkboxes.length).toBe(3)

    await user.click(checkboxes[0])
    await user.click(checkboxes[1])

    // Text is broken across elements, use a function matcher
    expect(screen.getByText((_content, element) => {
      return element?.textContent === "已选 2 项" && element?.tagName === "SPAN"
    })).toBeInTheDocument()

    // Third checkbox click should not increase count
    await user.click(checkboxes[2])
    expect(screen.getByText((_content, element) => {
      return element?.textContent === "已选 2 项" && element?.tagName === "SPAN"
    })).toBeInTheDocument()
  })

  it("'对比报价' button enabled when exactly 2 rows selected", async () => {
    const user = userEvent.setup()
    render(<CustomerQuotations quotations={mockQuotations} />)

    const checkboxes = screen.getAllByRole("checkbox")
    await user.click(checkboxes[0])

    const compareButton = screen.getByRole("button", { name: /对比报价/ })
    expect(compareButton).toBeDisabled()

    await user.click(checkboxes[1])
    expect(screen.getByRole("button", { name: /对比报价/ })).not.toBeDisabled()
  })

  it("QuotationCompareView shows side-by-side diff of two quotations", async () => {
    const user = userEvent.setup()
    const onLoadDetail = vi.fn()
      .mockResolvedValueOnce(mockDetailA)
      .mockResolvedValueOnce(mockDetailB)

    render(
      <CustomerQuotations
        quotations={mockQuotations}
        onLoadDetail={onLoadDetail}
      />,
    )

    const checkboxes = screen.getAllByRole("checkbox")
    await user.click(checkboxes[0])
    await user.click(checkboxes[1])
    await user.click(screen.getByRole("button", { name: /对比报价/ }))

    await waitFor(() => {
      expect(screen.getByText("LED Light A")).toBeInTheDocument()
    })
    expect(screen.getByText("LED Light B")).toBeInTheDocument()
  })

  it("diff highlights increased values with green styling", async () => {
    const user = userEvent.setup()
    const onLoadDetail = vi.fn()
      .mockResolvedValueOnce(mockDetailA)
      .mockResolvedValueOnce(mockDetailB)

    render(
      <CustomerQuotations
        quotations={mockQuotations}
        onLoadDetail={onLoadDetail}
      />,
    )

    const checkboxes = screen.getAllByRole("checkbox")
    await user.click(checkboxes[0])
    await user.click(checkboxes[1])
    await user.click(screen.getByRole("button", { name: /对比报价/ }))

    await waitFor(() => {
      expect(screen.getByText("LED Light A")).toBeInTheDocument()
    })

    // The total amount B ($18,000) > A ($15,000) should have green class
    const totalAmountCell = screen.getByText("$18,000.00").closest("td")
    expect(totalAmountCell?.className).toContain("bg-green")
  })
})
