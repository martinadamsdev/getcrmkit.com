import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it } from "vitest"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { http, HttpResponse } from "msw"
import { setupServer } from "msw/node"

import { CustomFieldManager } from "./CustomFieldManager"

const MOCK_DEFINITIONS = [
  { id: "d1", entity: "customer", name: "行业", type: "text", required: false, options: [], sort_order: 0 },
  { id: "d2", entity: "customer", name: "来源", type: "select", required: true, options: ["阿里巴巴", "展会"], sort_order: 1 },
]

const server = setupServer(
  http.get("/api/v1/custom-field-definitions", ({ request }) => {
    const url = new URL(request.url)
    const entity = url.searchParams.get("entity")
    const filtered = MOCK_DEFINITIONS.filter((d) => d.entity === entity)
    return HttpResponse.json({ items: filtered, total: filtered.length })
  }),
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

function renderWithProviders(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  })
  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>,
  )
}

describe("CustomFieldManager", () => {
  it("renders entity tabs (customer/product/contact)", () => {
    renderWithProviders(<CustomFieldManager />)
    expect(screen.getByRole("tab", { name: "客户" })).toBeInTheDocument()
    expect(screen.getByRole("tab", { name: "产品" })).toBeInTheDocument()
    expect(screen.getByRole("tab", { name: "联系人" })).toBeInTheDocument()
  })

  it("shows custom fields for selected entity", async () => {
    renderWithProviders(<CustomFieldManager />)
    await waitFor(() => {
      expect(screen.getByText("行业")).toBeInTheDocument()
      expect(screen.getByText("来源")).toBeInTheDocument()
    })
  })

  it("shows create field button", () => {
    renderWithProviders(<CustomFieldManager />)
    expect(screen.getByRole("button", { name: "新建字段" })).toBeInTheDocument()
  })

  it("opens create dialog on button click", async () => {
    const user = userEvent.setup()
    renderWithProviders(<CustomFieldManager />)
    await user.click(screen.getByRole("button", { name: "新建字段" }))
    await waitFor(() => {
      expect(screen.getByText("字段名")).toBeInTheDocument()
      // "类型" appears in both the table header and the dialog label
      expect(screen.getAllByText("类型").length).toBeGreaterThanOrEqual(2)
    })
  })
})
