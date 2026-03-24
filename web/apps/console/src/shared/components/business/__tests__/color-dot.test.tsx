import { render } from "@testing-library/react"
import { describe, expect, it } from "vitest"
import { ColorDot } from "../color-dot"

describe("ColorDot", () => {
  it("renders a dot with the given color", () => {
    const { container } = render(<ColorDot color="#ff0000" />)
    const dot = container.firstChild as HTMLElement
    expect(dot).toHaveStyle({ backgroundColor: "#ff0000" })
  })

  it("applies default size of 16px", () => {
    const { container } = render(<ColorDot color="#00ff00" />)
    const dot = container.firstChild as HTMLElement
    expect(dot).toHaveClass("h-4", "w-4")
  })

  it("supports sm size", () => {
    const { container } = render(<ColorDot color="#0000ff" size="sm" />)
    const dot = container.firstChild as HTMLElement
    expect(dot).toHaveClass("h-3", "w-3")
  })

  it("supports lg size", () => {
    const { container } = render(<ColorDot color="#ff00ff" size="lg" />)
    const dot = container.firstChild as HTMLElement
    expect(dot).toHaveClass("h-5", "w-5")
  })

  it("renders as a circle (rounded-full)", () => {
    const { container } = render(<ColorDot color="#000" />)
    const dot = container.firstChild as HTMLElement
    expect(dot).toHaveClass("rounded-full")
  })

  it("has accessible role and label", () => {
    const { container } = render(<ColorDot color="#ff0000" label="Red" />)
    const dot = container.firstChild as HTMLElement
    expect(dot).toHaveAttribute("aria-label", "Red")
  })

  it("accepts custom className", () => {
    const { container } = render(<ColorDot color="#000" className="mr-2" />)
    const dot = container.firstChild as HTMLElement
    expect(dot).toHaveClass("mr-2")
  })
})
