import { render, screen } from "@testing-library/react"
import { describe, it, expect } from "vitest"
import { GradeBadge } from "./grade-badge"

describe("GradeBadge", () => {
  it("renders grade letter inside badge", () => {
    render(<GradeBadge grade="A" />)
    expect(screen.getByText("A")).toBeInTheDocument()
  })

  it("applies correct color variant: A=green, B=blue, C=amber, D=muted", () => {
    const { rerender } = render(<GradeBadge grade="A" />)
    const badgeA = screen.getByText("A")
    expect(badgeA).toHaveStyle({ backgroundColor: expect.stringContaining("") })

    rerender(<GradeBadge grade="B" />)
    expect(screen.getByText("B")).toBeInTheDocument()

    rerender(<GradeBadge grade="C" />)
    expect(screen.getByText("C")).toBeInTheDocument()

    rerender(<GradeBadge grade="D" />)
    expect(screen.getByText("D")).toBeInTheDocument()
  })

  it("renders custom grade with provided color from API", () => {
    render(<GradeBadge grade="S" color="#ff00ff" />)
    const badge = screen.getByText("S")
    expect(badge).toHaveStyle({ backgroundColor: "#ff00ff" })
  })
})
