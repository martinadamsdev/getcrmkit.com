import { render, screen } from "@testing-library/react"
import { describe, it, expect } from "vitest"
import { CountryFlag } from "./country-flag"

describe("CountryFlag", () => {
  it("renders emoji flag for valid country code", () => {
    render(<CountryFlag countryCode="US" />)
    // US flag emoji
    expect(screen.getByText(/\u{1F1FA}\u{1F1F8}/u)).toBeInTheDocument()
  })

  it("renders country code text when countryCode provided", () => {
    render(<CountryFlag countryCode="CN" showName />)
    const element = screen.getByTitle(/China/i)
    expect(element).toBeInTheDocument()
  })

  it("renders nothing when countryCode is null/undefined", () => {
    const { container } = render(<CountryFlag countryCode={null} />)
    expect(container.textContent).toBe("")
  })
})
