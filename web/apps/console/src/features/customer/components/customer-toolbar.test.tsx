import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import { CustomerToolbar } from "./customer-toolbar"

describe("CustomerToolbar", () => {
  const defaultProps = {
    onSearch: vi.fn(),
    onFilterClick: vi.fn(),
    activeFilterCount: 0,
    onCreateClick: vi.fn(),
    onImportClick: vi.fn(),
    onExportClick: vi.fn(),
  }

  it("renders search input, create button, import button, and export button", () => {
    render(<CustomerToolbar {...defaultProps} />)

    expect(
      screen.getByPlaceholderText("搜索客户名/联系人/邮箱..."),
    ).toBeInTheDocument()
    expect(screen.getByRole("button", { name: /新建客户/ })).toBeInTheDocument()
    expect(screen.getByRole("button", { name: /导入/ })).toBeInTheDocument()
    expect(screen.getByRole("button", { name: /导出/ })).toBeInTheDocument()
  })

  it("calls onSearch when search value changes after debounce", async () => {
    const onSearch = vi.fn()
    render(<CustomerToolbar {...defaultProps} onSearch={onSearch} />)

    const input = screen.getByPlaceholderText("搜索客户名/联系人/邮箱...")
    await userEvent.type(input, "Acme")

    // Wait for debounce (500ms) to fire
    await waitFor(() => {
      expect(onSearch).toHaveBeenCalledWith("Acme")
    }, { timeout: 1000 })
  })

  it("calls onCreateClick when '新建客户' button clicked", async () => {
    const onCreateClick = vi.fn()
    render(<CustomerToolbar {...defaultProps} onCreateClick={onCreateClick} />)

    await userEvent.click(screen.getByRole("button", { name: /新建客户/ }))
    expect(onCreateClick).toHaveBeenCalledOnce()
  })

  it("calls onExportClick when export button clicked", async () => {
    const onExportClick = vi.fn()
    render(<CustomerToolbar {...defaultProps} onExportClick={onExportClick} />)

    await userEvent.click(screen.getByRole("button", { name: /导出/ }))
    expect(onExportClick).toHaveBeenCalledOnce()
  })
})
