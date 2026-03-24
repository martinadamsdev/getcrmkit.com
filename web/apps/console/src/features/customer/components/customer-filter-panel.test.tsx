import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import { CustomerFilterPanel } from "./customer-filter-panel"
import type { CustomerFilters } from "../types"

describe("CustomerFilterPanel", () => {
  const emptyFilters: CustomerFilters = {
    grade_id: null,
    source: null,
    country: null,
    industry: null,
    follow_status: null,
  }

  it("renders filter groups: grade, source, country, industry, follow status", () => {
    render(
      <CustomerFilterPanel
        filters={emptyFilters}
        onChange={vi.fn()}
        onReset={vi.fn()}
      />,
    )

    expect(screen.getByText("等级")).toBeInTheDocument()
    expect(screen.getByText("来源")).toBeInTheDocument()
    expect(screen.getByText("国家")).toBeInTheDocument()
    expect(screen.getByText("行业")).toBeInTheDocument()
    expect(screen.getByText("跟进状态")).toBeInTheDocument()
  })

  it("renders grade toggle options with GradeBadge", () => {
    render(
      <CustomerFilterPanel
        filters={emptyFilters}
        onChange={vi.fn()}
        onReset={vi.fn()}
      />,
    )

    expect(screen.getByLabelText("Grade A")).toBeInTheDocument()
    expect(screen.getByLabelText("Grade B")).toBeInTheDocument()
    expect(screen.getByLabelText("Grade C")).toBeInTheDocument()
    expect(screen.getByLabelText("Grade D")).toBeInTheDocument()
  })

  it("calls onChange when a grade is selected", async () => {
    const user = userEvent.setup()
    const onChange = vi.fn()

    render(
      <CustomerFilterPanel
        filters={emptyFilters}
        onChange={onChange}
        onReset={vi.fn()}
      />,
    )

    await user.click(screen.getByLabelText("Grade A"))
    expect(onChange).toHaveBeenCalledWith("grade_id", "A")
  })

  it("shows '清除全部筛选' button when filters are active and calls onReset", async () => {
    const user = userEvent.setup()
    const onReset = vi.fn()

    render(
      <CustomerFilterPanel
        filters={{ ...emptyFilters, source: "alibaba" }}
        onChange={vi.fn()}
        onReset={onReset}
      />,
    )

    const clearButton = screen.getByText("清除全部筛选")
    expect(clearButton).toBeInTheDocument()
    await user.click(clearButton)
    expect(onReset).toHaveBeenCalledOnce()
  })
})
