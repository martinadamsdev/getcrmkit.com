import { render, screen } from "@testing-library/react"
import { describe, expect, it, vi } from "vitest"
import { ProductTable } from "../product-table"

const MOCK_PRODUCTS = [
  {
    id: "prod-1",
    name: "Stainless Steel Tumbler",
    sku: "SST-001",
    category_name: "水杯",
    image_url: "https://example.com/tumbler.jpg",
    cost_price: "45.50",
    cost_currency: "CNY",
    selling_price: "12.99",
    selling_currency: "USD",
    variant_count: 3,
    is_active: true,
    created_at: "2026-03-01T10:00:00Z",
  },
  {
    id: "prod-2",
    name: "Bamboo Cutting Board",
    sku: "BCB-002",
    category_name: "厨具",
    image_url: null,
    cost_price: "25.00",
    cost_currency: "CNY",
    selling_price: "8.50",
    selling_currency: "USD",
    variant_count: 0,
    is_active: true,
    created_at: "2026-03-02T10:00:00Z",
  },
]

describe("ProductTable", () => {
  it("renders table headers", () => {
    render(
      <ProductTable
        data={MOCK_PRODUCTS}
        total={2}
        page={1}
        pageSize={20}
        onPageChange={() => {}}
        onRowClick={() => {}}
      />,
    )
    expect(screen.getByText("产品")).toBeInTheDocument()
    expect(screen.getByText("SKU")).toBeInTheDocument()
    expect(screen.getByText("分类")).toBeInTheDocument()
    expect(screen.getByText("成本")).toBeInTheDocument()
    expect(screen.getByText("售价")).toBeInTheDocument()
    expect(screen.getByText("变体")).toBeInTheDocument()
  })

  it("renders product rows", () => {
    render(
      <ProductTable
        data={MOCK_PRODUCTS}
        total={2}
        page={1}
        pageSize={20}
        onPageChange={() => {}}
        onRowClick={() => {}}
      />,
    )
    expect(screen.getByText("Stainless Steel Tumbler")).toBeInTheDocument()
    expect(screen.getByText("SST-001")).toBeInTheDocument()
    expect(screen.getByText("水杯")).toBeInTheDocument()
    expect(screen.getByText("¥45.50")).toBeInTheDocument()
    expect(screen.getByText("$12.99")).toBeInTheDocument()
    expect(screen.getByText("3")).toBeInTheDocument()
  })

  it("renders thumbnail placeholder for missing images", () => {
    render(
      <ProductTable
        data={MOCK_PRODUCTS}
        total={2}
        page={1}
        pageSize={20}
        onPageChange={() => {}}
        onRowClick={() => {}}
      />,
    )
    const avatars = screen.getAllByText("Stainless Steel Tumbler")
    expect(avatars.length).toBeGreaterThanOrEqual(1)
  })

  it("calls onRowClick when row clicked", async () => {
    const onRowClick = vi.fn()
    const { container } = render(
      <ProductTable
        data={MOCK_PRODUCTS}
        total={2}
        page={1}
        pageSize={20}
        onPageChange={() => {}}
        onRowClick={onRowClick}
      />,
    )
    const rows = container.querySelectorAll("tbody tr")
    rows[0]?.click()
    expect(onRowClick).toHaveBeenCalledWith("prod-1")
  })

  it("renders empty state", () => {
    render(
      <ProductTable
        data={[]}
        total={0}
        page={1}
        pageSize={20}
        onPageChange={() => {}}
        onRowClick={() => {}}
      />,
    )
    expect(screen.getByText(/暂无产品/)).toBeInTheDocument()
  })
})
