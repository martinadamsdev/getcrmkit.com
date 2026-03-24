import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, it, expect, vi } from "vitest"
import { DateRangePicker } from "./date-range-picker"

describe("DateRangePicker", () => {
  it('renders with placeholder when no date selected', () => {
    render(<DateRangePicker onChange={vi.fn()} />)
    expect(screen.getByText(/select date range/i)).toBeInTheDocument()
  })

  it("displays formatted date range when range is set", () => {
    const from = new Date(2026, 0, 1)
    const to = new Date(2026, 0, 31)
    render(<DateRangePicker value={{ from, to }} onChange={vi.fn()} />)
    expect(screen.getByText(/2026-01-01/)).toBeInTheDocument()
    expect(screen.getByText(/2026-01-31/)).toBeInTheDocument()
  })

  it("opens calendar popover when trigger clicked", async () => {
    const user = userEvent.setup()
    render(<DateRangePicker onChange={vi.fn()} />)
    await user.click(screen.getByRole("button"))
    // Calendar renders with data-slot="calendar"
    expect(document.querySelector('[data-slot="calendar"]')).toBeInTheDocument()
  })
})
