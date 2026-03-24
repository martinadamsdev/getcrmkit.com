import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import { SavedViewTabs } from "./saved-view-tabs"
import type { SavedView } from "../types"

const mockViews: SavedView[] = [
  {
    id: "view-1",
    name: "A级客户",
    entity: "customer",
    filter_config: { grade_id: "A" },
    created_at: "2026-01-01T00:00:00Z",
  },
  {
    id: "view-2",
    name: "Alibaba来源",
    entity: "customer",
    filter_config: { source: "alibaba" },
    created_at: "2026-01-02T00:00:00Z",
  },
]

describe("SavedViewTabs", () => {
  const defaultProps = {
    views: mockViews,
    onViewChange: vi.fn(),
    onSave: vi.fn(),
    onDelete: vi.fn(),
  }

  it("renders '全部' tab + saved view tabs", () => {
    render(<SavedViewTabs {...defaultProps} />)

    expect(screen.getByText("全部")).toBeInTheDocument()
    expect(screen.getByText("A级客户")).toBeInTheDocument()
    expect(screen.getByText("Alibaba来源")).toBeInTheDocument()
  })

  it("calls onViewChange with filter_config when a saved view tab clicked", async () => {
    const user = userEvent.setup()
    const onViewChange = vi.fn()

    render(<SavedViewTabs {...defaultProps} onViewChange={onViewChange} />)

    await user.click(screen.getByText("A级客户"))
    expect(onViewChange).toHaveBeenCalledWith({ grade_id: "A" })
  })

  it("calls onViewChange with empty object when '全部' tab clicked", async () => {
    const user = userEvent.setup()
    const onViewChange = vi.fn()

    render(
      <SavedViewTabs
        {...defaultProps}
        activeViewId="view-1"
        onViewChange={onViewChange}
      />,
    )

    await user.click(screen.getByText("全部"))
    expect(onViewChange).toHaveBeenCalledWith({})
  })

  it("opens save dialog when + button clicked and calls onSave", async () => {
    const user = userEvent.setup()
    const onSave = vi.fn()

    render(<SavedViewTabs {...defaultProps} onSave={onSave} />)

    await user.click(screen.getByLabelText("Save current view"))
    expect(screen.getByText("保存当前视图")).toBeInTheDocument()

    const input = screen.getByPlaceholderText("输入视图名称")
    await user.type(input, "我的视图")
    await user.click(screen.getByRole("button", { name: "保存" }))
    expect(onSave).toHaveBeenCalledWith("我的视图")
  })
})
