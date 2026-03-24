import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import { ProductToolbar } from "../product-toolbar"

describe("ProductToolbar", () => {
  const defaultProps = {
    onSearch: vi.fn(),
    onCreateClick: vi.fn(),
    onImportClick: vi.fn(),
    onExportClick: vi.fn(),
  }

  it("renders search input", () => {
    render(<ProductToolbar {...defaultProps} />)
    expect(screen.getByPlaceholderText("搜索产品...")).toBeInTheDocument()
  })

  it("renders create button", () => {
    render(<ProductToolbar {...defaultProps} />)
    expect(
      screen.getByRole("button", { name: /新建产品/ }),
    ).toBeInTheDocument()
  })

  it("renders import and export buttons", () => {
    render(<ProductToolbar {...defaultProps} />)
    expect(screen.getByRole("button", { name: /导入/ })).toBeInTheDocument()
    expect(screen.getByRole("button", { name: /导出/ })).toBeInTheDocument()
  })

  it("calls onCreateClick when button clicked", async () => {
    const user = userEvent.setup()
    render(<ProductToolbar {...defaultProps} />)
    await user.click(screen.getByRole("button", { name: /新建产品/ }))
    expect(defaultProps.onCreateClick).toHaveBeenCalledOnce()
  })
})
