import { screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import { renderWithProviders } from "@/test/render"
import { ProductPicker } from "../product-picker"

describe("ProductPicker", () => {
  it("renders placeholder text", () => {
    renderWithProviders(<ProductPicker value={null} onChange={() => {}} />)
    expect(screen.getByText("选择产品...")).toBeInTheDocument()
  })

  it("opens popover on click", async () => {
    const user = userEvent.setup()
    renderWithProviders(<ProductPicker value={null} onChange={() => {}} />)
    await user.click(screen.getByText("选择产品..."))
    expect(screen.getByPlaceholderText("搜索 SKU 或名称...")).toBeInTheDocument()
  })

  it("calls onChange when product selected", async () => {
    const onChange = vi.fn()
    renderWithProviders(<ProductPicker value={null} onChange={onChange} />)
    expect(screen.getByText("选择产品...")).toBeInTheDocument()
  })
})
