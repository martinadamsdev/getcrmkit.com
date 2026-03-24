import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, it, expect, vi, beforeAll, afterAll, afterEach } from "vitest"
import { http, HttpResponse } from "msw"
import { setupServer } from "msw/node"
import { renderWithProviders } from "@/test/render"
import { CustomerPicker } from "./customer-picker"

const server = setupServer(
  http.get("/api/v1/customers", ({ request }) => {
    const url = new URL(request.url)
    const keyword = url.searchParams.get("keyword")
    if (keyword === "empty") {
      return HttpResponse.json({ items: [], total: 0 })
    }
    return HttpResponse.json({
      items: [
        { id: "c1", company_name: "Acme Corp", country: "US", grade: "A" },
        { id: "c2", company_name: "Beta Inc", country: "CN", grade: "B" },
      ],
      total: 2,
    })
  }),
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe("CustomerPicker", () => {
  it("renders combobox trigger", () => {
    renderWithProviders(<CustomerPicker onChange={vi.fn()} />)
    expect(screen.getByRole("button")).toBeInTheDocument()
  })

  it("shows selected customer name when value provided", () => {
    renderWithProviders(
      <CustomerPicker
        value="c1"
        displayName="Acme Corp"
        onChange={vi.fn()}
      />,
    )
    expect(screen.getByText("Acme Corp")).toBeInTheDocument()
  })

  it("shows no customers found for empty results", async () => {
    const user = userEvent.setup()
    renderWithProviders(<CustomerPicker onChange={vi.fn()} />)
    await user.click(screen.getByRole("button"))
    const input = screen.getByPlaceholderText(/search/i)
    await user.type(input, "empty")
    await waitFor(() => {
      expect(screen.getByText(/no customers/i)).toBeInTheDocument()
    })
  })

  it("calls onChange with selected customer", async () => {
    const user = userEvent.setup()
    const onChange = vi.fn()
    renderWithProviders(<CustomerPicker onChange={onChange} />)
    await user.click(screen.getByRole("button"))
    const input = screen.getByPlaceholderText(/search/i)
    await user.type(input, "acme")
    await waitFor(() => {
      expect(screen.getByText("Acme Corp")).toBeInTheDocument()
    })
    await user.click(screen.getByText("Acme Corp"))
    expect(onChange).toHaveBeenCalledWith("c1", "Acme Corp")
  })
})
