import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import { VariantTable } from "../variant-table"

const MOCK_VARIANTS = [
  {
    id: "var-1",
    material: "Stainless Steel",
    color: "#C0C0C0",
    color_name: "Silver",
    size: "350ml",
    sku: "SST-001-S",
    cost_price: "40.00",
  },
  {
    id: "var-2",
    material: "Stainless Steel",
    color: "#000000",
    color_name: "Black",
    size: "500ml",
    sku: "SST-001-B",
    cost_price: "45.00",
  },
]

describe("VariantTable", () => {
  it("renders table headers", () => {
    render(
      <VariantTable
        variants={MOCK_VARIANTS}
        onAdd={() => {}}
        onUpdate={() => {}}
        onDelete={() => {}}
      />,
    )
    expect(screen.getByText("材质")).toBeInTheDocument()
    expect(screen.getByText("颜色")).toBeInTheDocument()
    expect(screen.getByText("尺寸")).toBeInTheDocument()
    expect(screen.getByText("SKU")).toBeInTheDocument()
    expect(screen.getByText("成本")).toBeInTheDocument()
  })

  it("renders variant rows", () => {
    render(
      <VariantTable
        variants={MOCK_VARIANTS}
        onAdd={() => {}}
        onUpdate={() => {}}
        onDelete={() => {}}
      />,
    )
    expect(screen.getByText("Silver")).toBeInTheDocument()
    expect(screen.getByText("350ml")).toBeInTheDocument()
    expect(screen.getByText("SST-001-S")).toBeInTheDocument()
  })

  it("renders color dots", () => {
    render(
      <VariantTable
        variants={MOCK_VARIANTS}
        onAdd={() => {}}
        onUpdate={() => {}}
        onDelete={() => {}}
      />,
    )
    expect(screen.getByLabelText("Silver")).toBeInTheDocument()
    expect(screen.getByLabelText("Black")).toBeInTheDocument()
  })

  it("renders add variant button", () => {
    render(
      <VariantTable
        variants={MOCK_VARIANTS}
        onAdd={() => {}}
        onUpdate={() => {}}
        onDelete={() => {}}
      />,
    )
    expect(
      screen.getByRole("button", { name: /添加变体/ }),
    ).toBeInTheDocument()
  })

  it("calls onAdd when add button clicked", async () => {
    const user = userEvent.setup()
    const onAdd = vi.fn()
    render(
      <VariantTable
        variants={MOCK_VARIANTS}
        onAdd={onAdd}
        onUpdate={() => {}}
        onDelete={() => {}}
      />,
    )
    await user.click(screen.getByRole("button", { name: /添加变体/ }))
    expect(onAdd).toHaveBeenCalledOnce()
  })

  it("renders delete buttons for each row", () => {
    render(
      <VariantTable
        variants={MOCK_VARIANTS}
        onAdd={() => {}}
        onUpdate={() => {}}
        onDelete={() => {}}
      />,
    )
    const deleteButtons = screen.getAllByRole("button", { name: /删除/ })
    expect(deleteButtons).toHaveLength(2)
  })

  it("renders empty state when no variants", () => {
    render(
      <VariantTable
        variants={[]}
        onAdd={() => {}}
        onUpdate={() => {}}
        onDelete={() => {}}
      />,
    )
    expect(screen.getByText(/暂无变体/)).toBeInTheDocument()
  })
})
