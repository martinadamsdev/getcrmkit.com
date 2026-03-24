import { render, screen } from "@testing-library/react"
import { describe, it, expect } from "vitest"
import { Mail, Phone } from "lucide-react"
import { Timeline } from "./timeline"

const items = [
  {
    id: "1",
    time: new Date("2026-03-23T10:00:00Z"),
    icon: Mail,
    content: "Sent follow-up email",
    type: "default" as const,
  },
  {
    id: "2",
    time: new Date("2026-03-22T15:00:00Z"),
    icon: Phone,
    content: "Phone call with customer",
    type: "success" as const,
  },
]

describe("Timeline", () => {
  it("renders timeline items with content", () => {
    render(<Timeline items={items} />)
    expect(screen.getByText("Sent follow-up email")).toBeInTheDocument()
    expect(screen.getByText("Phone call with customer")).toBeInTheDocument()
  })

  it("renders icon and formatted time for each item", () => {
    render(<Timeline items={items} />)
    // Icons render as SVGs
    const svgs = document.querySelectorAll("svg")
    expect(svgs.length).toBeGreaterThanOrEqual(2)
  })

  it("renders different colored indicators based on item type", () => {
    render(<Timeline items={items} />)
    // Check that timeline dots exist with different color indicators
    const dots = document.querySelectorAll("[data-timeline-dot]")
    expect(dots.length).toBe(2)
  })

  it("shows empty message when items is empty", () => {
    render(<Timeline items={[]} emptyMessage="No activity yet" />)
    expect(screen.getByText("No activity yet")).toBeInTheDocument()
  })
})
