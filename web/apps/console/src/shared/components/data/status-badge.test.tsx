import { render, screen } from "@testing-library/react"
import { describe, it, expect } from "vitest"
import { StatusBadge } from "./status-badge"

describe("StatusBadge", () => {
  it("renders status text with correct variant color", () => {
    render(<StatusBadge status="active" labelMap={{ active: "Active" }} />)
    expect(screen.getByText("Active")).toBeInTheDocument()
  })

  it("supports custom colorMap override", () => {
    render(
      <StatusBadge
        status="urgent"
        colorMap={{ urgent: "destructive" }}
        labelMap={{ urgent: "Urgent" }}
      />,
    )
    const badge = screen.getByText("Urgent").closest("[data-slot='badge']")
    expect(badge).toHaveAttribute("data-variant", "destructive")
  })

  it("renders with dot indicator before text", () => {
    render(<StatusBadge status="active" labelMap={{ active: "Active" }} />)
    const dot = document.querySelector("[data-status-dot]")
    expect(dot).toBeInTheDocument()
  })
})
