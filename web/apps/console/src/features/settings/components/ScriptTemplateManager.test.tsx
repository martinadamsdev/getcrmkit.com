import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it } from "vitest"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { http, HttpResponse } from "msw"
import { setupServer } from "msw/node"

import { ScriptTemplateManager } from "./ScriptTemplateManager"

const MOCK_TEMPLATES = [
  {
    id: "t1",
    scene: "first_contact",
    content: "System first contact template",
    is_system: true,
  },
  {
    id: "t2",
    scene: "first_contact",
    content: "My custom first contact",
    is_system: false,
  },
]

const server = setupServer(
  http.get("/api/v1/script-templates", () =>
    HttpResponse.json({ items: MOCK_TEMPLATES, total: 2 }),
  ),
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

describe("ScriptTemplateManager", () => {
  it("renders system and user template sections", async () => {
    renderWithProviders(<ScriptTemplateManager />)
    await waitFor(() => {
      expect(screen.getByText("系统模板")).toBeInTheDocument()
      expect(screen.getByText("我的模板")).toBeInTheDocument()
    })
  })

  it("shows system templates as read-only", async () => {
    renderWithProviders(<ScriptTemplateManager />)
    await waitFor(() => {
      expect(screen.getByText("System first contact template")).toBeInTheDocument()
    })
    expect(screen.getByText("系统模板不可编辑")).toBeInTheDocument()
  })

  it("shows create template button", async () => {
    renderWithProviders(<ScriptTemplateManager />)
    await waitFor(() => {
      expect(screen.getByRole("button", { name: "新建模板" })).toBeInTheDocument()
    })
  })

  it("opens create dialog on button click", async () => {
    const user = userEvent.setup()
    renderWithProviders(<ScriptTemplateManager />)
    await waitFor(() => {
      expect(screen.getByRole("button", { name: "新建模板" })).toBeInTheDocument()
    })
    await user.click(screen.getByRole("button", { name: "新建模板" }))
    expect(screen.getByText("场景")).toBeInTheDocument()
    expect(screen.getByText("内容")).toBeInTheDocument()
  })
})
