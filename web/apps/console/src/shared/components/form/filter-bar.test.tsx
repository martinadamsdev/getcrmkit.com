import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, it, expect, vi } from "vitest"
import { FilterBar } from "./filter-bar"
import type { FilterDef } from "@/shared/hooks/use-filters"

const filters: FilterDef[] = [
  {
    key: "grade",
    label: "Grade",
    type: "select",
    options: [
      { label: "A", value: "A" },
      { label: "B", value: "B" },
    ],
  },
  { key: "country", label: "Country", type: "text" },
]

describe("FilterBar", () => {
  it("renders filter trigger button with count of active filters", () => {
    render(
      <FilterBar
        filters={filters}
        values={{ grade: "A", country: null }}
        onChange={vi.fn()}
        onReset={vi.fn()}
      />,
    )
    const trigger = screen.getByRole("button", { name: /filter/i })
    expect(trigger).toBeInTheDocument()
    expect(screen.getByText("1")).toBeInTheDocument()
  })

  it("opens popover with filter controls on click", async () => {
    const user = userEvent.setup()
    render(
      <FilterBar
        filters={filters}
        values={{ grade: null, country: null }}
        onChange={vi.fn()}
        onReset={vi.fn()}
      />,
    )
    await user.click(screen.getByRole("button", { name: /filter/i }))
    // Grade appears as label + select placeholder
    expect(screen.getAllByText("Grade").length).toBeGreaterThanOrEqual(1)
    expect(screen.getByPlaceholderText("Country")).toBeInTheDocument()
  })

  it("calls onChange when a filter value is entered", async () => {
    const user = userEvent.setup()
    const onChange = vi.fn()
    render(
      <FilterBar
        filters={filters}
        values={{ grade: null, country: null }}
        onChange={onChange}
        onReset={vi.fn()}
      />,
    )
    await user.click(screen.getByRole("button", { name: /filter/i }))
    const countryInput = screen.getByPlaceholderText("Country")
    await user.type(countryInput, "U")
    expect(onChange).toHaveBeenCalledWith("country", "U")
  })

  it("shows clear filters button when any filter active", async () => {
    const user = userEvent.setup()
    const onReset = vi.fn()
    render(
      <FilterBar
        filters={filters}
        values={{ grade: "A", country: null }}
        onChange={vi.fn()}
        onReset={onReset}
      />,
    )
    await user.click(screen.getByRole("button", { name: /filter/i }))
    const clearButton = screen.getByRole("button", { name: /clear/i })
    expect(clearButton).toBeInTheDocument()
    await user.click(clearButton)
    expect(onReset).toHaveBeenCalledOnce()
  })
})
