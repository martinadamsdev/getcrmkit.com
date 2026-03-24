import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, it, expect, vi } from "vitest"
import { SearchInput } from "./search-input"

describe("SearchInput", () => {
  it("renders input with placeholder", () => {
    render(<SearchInput onSearch={vi.fn()} placeholder="Search customers" />)
    expect(
      screen.getByPlaceholderText("Search customers"),
    ).toBeInTheDocument()
  })

  it("calls onSearch after debounce delay", async () => {
    const user = userEvent.setup()
    const onSearch = vi.fn()
    render(<SearchInput onSearch={onSearch} debounceMs={100} />)
    const input = screen.getByRole("textbox")
    await user.type(input, "hello")
    await waitFor(() => {
      expect(onSearch).toHaveBeenCalledWith("hello")
    })
  })

  it("shows search icon", () => {
    render(<SearchInput onSearch={vi.fn()} />)
    const svg = document.querySelector("svg")
    expect(svg).toBeInTheDocument()
  })

  it("clears input when X button clicked and calls onSearch with empty string", async () => {
    const user = userEvent.setup()
    const onSearch = vi.fn()
    render(<SearchInput onSearch={onSearch} debounceMs={100} />)
    const input = screen.getByRole("textbox")
    await user.type(input, "test")
    await waitFor(() => {
      expect(onSearch).toHaveBeenCalledWith("test")
    })
    onSearch.mockClear()

    const clearButton = screen.getByRole("button", { name: /clear/i })
    await user.click(clearButton)
    await waitFor(() => {
      expect(onSearch).toHaveBeenCalledWith("")
    })
    expect(input).toHaveValue("")
  })
})
