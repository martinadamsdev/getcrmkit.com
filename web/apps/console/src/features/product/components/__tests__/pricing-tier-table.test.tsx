import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import { PricingTierTable } from "../pricing-tier-table"

const MOCK_TIERS = [
  { id: "tier-1", min_qty: 1, max_qty: 99, multiplier: "1.50" },
  { id: "tier-2", min_qty: 100, max_qty: 499, multiplier: "1.36" },
  { id: "tier-3", min_qty: 500, max_qty: null, multiplier: "1.20" },
]

describe("PricingTierTable", () => {
  it("renders table headers", () => {
    render(
      <PricingTierTable
        tiers={MOCK_TIERS}
        onAdd={() => {}}
        onUpdate={() => {}}
        onDelete={() => {}}
      />,
    )
    expect(screen.getByText("最小数量")).toBeInTheDocument()
    expect(screen.getByText("最大数量")).toBeInTheDocument()
    expect(screen.getByText("倍率")).toBeInTheDocument()
  })

  it("renders tier rows with values", () => {
    render(
      <PricingTierTable
        tiers={MOCK_TIERS}
        onAdd={() => {}}
        onUpdate={() => {}}
        onDelete={() => {}}
      />,
    )
    expect(screen.getByDisplayValue("1")).toBeInTheDocument()
    expect(screen.getByDisplayValue("99")).toBeInTheDocument()
    expect(screen.getByDisplayValue("1.50")).toBeInTheDocument()
  })

  it("renders add tier button", () => {
    render(
      <PricingTierTable
        tiers={MOCK_TIERS}
        onAdd={() => {}}
        onUpdate={() => {}}
        onDelete={() => {}}
      />,
    )
    expect(
      screen.getByRole("button", { name: /添加阶梯/ }),
    ).toBeInTheDocument()
  })

  it("calls onAdd when add button clicked", async () => {
    const user = userEvent.setup()
    const onAdd = vi.fn()
    render(
      <PricingTierTable
        tiers={MOCK_TIERS}
        onAdd={onAdd}
        onUpdate={() => {}}
        onDelete={() => {}}
      />,
    )
    await user.click(screen.getByRole("button", { name: /添加阶梯/ }))
    expect(onAdd).toHaveBeenCalledOnce()
  })

  it("renders multiplier display format", () => {
    render(
      <PricingTierTable
        tiers={MOCK_TIERS}
        onAdd={() => {}}
        onUpdate={() => {}}
        onDelete={() => {}}
      />,
    )
    expect(screen.getByDisplayValue("1.50")).toBeInTheDocument()
    expect(screen.getByDisplayValue("1.36")).toBeInTheDocument()
    expect(screen.getByDisplayValue("1.20")).toBeInTheDocument()
  })
})
