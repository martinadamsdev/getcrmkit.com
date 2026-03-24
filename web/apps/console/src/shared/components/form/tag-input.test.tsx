import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, it, expect, vi } from "vitest"
import { TagInput } from "./tag-input"

describe("TagInput", () => {
  const tags = [
    { name: "VIP", color: "#ff0000" },
    { name: "New", color: "#00ff00" },
  ]

  it("renders existing tags as badge elements", () => {
    render(<TagInput tags={tags} onAdd={vi.fn()} onRemove={vi.fn()} />)
    expect(screen.getByText("VIP")).toBeInTheDocument()
    expect(screen.getByText("New")).toBeInTheDocument()
  })

  it("shows input field for typing new tag name", () => {
    render(<TagInput tags={[]} onAdd={vi.fn()} onRemove={vi.fn()} />)
    expect(screen.getByPlaceholderText(/add tag/i)).toBeInTheDocument()
  })

  it("calls onAdd with tag name and color when Enter pressed", async () => {
    const user = userEvent.setup()
    const onAdd = vi.fn()
    render(<TagInput tags={[]} onAdd={onAdd} onRemove={vi.fn()} />)
    const input = screen.getByPlaceholderText(/add tag/i)
    await user.type(input, "Important{Enter}")
    expect(onAdd).toHaveBeenCalledWith(
      expect.objectContaining({ name: "Important" }),
    )
  })

  it("calls onRemove when tag X button clicked", async () => {
    const user = userEvent.setup()
    const onRemove = vi.fn()
    render(<TagInput tags={tags} onAdd={vi.fn()} onRemove={onRemove} />)
    const removeButtons = screen.getAllByRole("button", { name: /remove/i })
    await user.click(removeButtons[0])
    expect(onRemove).toHaveBeenCalledWith(0)
  })

  it("shows color picker popover when color dot clicked", async () => {
    const user = userEvent.setup()
    render(<TagInput tags={[]} onAdd={vi.fn()} onRemove={vi.fn()} />)
    const colorButton = screen.getByRole("button", { name: /color/i })
    await user.click(colorButton)
    // react-colorful renders a div with role="slider"
    expect(document.querySelector(".react-colorful")).toBeInTheDocument()
  })
})
