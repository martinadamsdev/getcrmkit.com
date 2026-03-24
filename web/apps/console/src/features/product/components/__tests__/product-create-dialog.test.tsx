import { render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"
import { renderWithProviders } from "@/test/render"
import { ProductCreateDialog } from "../product-create-dialog"

describe("ProductCreateDialog", () => {
  it("renders dialog title when open", () => {
    renderWithProviders(
      <ProductCreateDialog open onOpenChange={() => {}} />,
    )
    expect(screen.getByText("新建产品")).toBeInTheDocument()
  })

  it("renders name input", () => {
    renderWithProviders(
      <ProductCreateDialog open onOpenChange={() => {}} />,
    )
    expect(screen.getByPlaceholderText("产品名称")).toBeInTheDocument()
  })

  it("renders SKU input", () => {
    renderWithProviders(
      <ProductCreateDialog open onOpenChange={() => {}} />,
    )
    expect(screen.getByPlaceholderText("SKU 编码")).toBeInTheDocument()
  })

  it("renders cost and price inputs", () => {
    renderWithProviders(
      <ProductCreateDialog open onOpenChange={() => {}} />,
    )
    expect(screen.getByPlaceholderText("成本价 (CNY)")).toBeInTheDocument()
    expect(screen.getByPlaceholderText("售价 (USD)")).toBeInTheDocument()
  })

  it("renders save button", () => {
    renderWithProviders(
      <ProductCreateDialog open onOpenChange={() => {}} />,
    )
    expect(screen.getByRole("button", { name: /保存/ })).toBeInTheDocument()
  })

  it("does not render when closed", () => {
    renderWithProviders(
      <ProductCreateDialog open={false} onOpenChange={() => {}} />,
    )
    expect(screen.queryByText("新建产品")).not.toBeInTheDocument()
  })
})
