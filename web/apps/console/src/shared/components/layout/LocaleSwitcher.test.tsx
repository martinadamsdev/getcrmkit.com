import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it } from "vitest"

import { LocaleSwitcher } from "./LocaleSwitcher"

describe("LocaleSwitcher", () => {
  it("renders a button", () => {
    render(<LocaleSwitcher />)
    expect(screen.getByRole("button")).toBeInTheDocument()
  })

  it("shows locale options on click", async () => {
    const user = userEvent.setup()
    render(<LocaleSwitcher />)
    await user.click(screen.getByRole("button"))
    expect(screen.getByText("中文")).toBeInTheDocument()
    expect(screen.getByText("English")).toBeInTheDocument()
  })
})
