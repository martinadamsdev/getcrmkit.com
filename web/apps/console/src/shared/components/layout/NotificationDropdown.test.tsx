import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it } from "vitest"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { http, HttpResponse } from "msw"
import { setupServer } from "msw/node"

import { NotificationDropdown } from "./NotificationDropdown"

const MOCK_NOTIFICATIONS = {
  items: [
    { id: "n1", title: "客户到期提醒", body: "客户 ABC 已超过15天未跟进", read: false, created_at: "2026-03-22T10:00:00Z" },
    { id: "n2", title: "发货预警", body: "订单 ORD-001 即将到期", read: false, created_at: "2026-03-21T08:00:00Z" },
  ],
  total: 2,
}

const server = setupServer(
  http.get("/api/v1/notifications", () => HttpResponse.json(MOCK_NOTIFICATIONS)),
  http.patch("/api/v1/notifications/:id/read", () => HttpResponse.json({ success: true })),
  http.post("/api/v1/notifications/read-all", () => HttpResponse.json({ success: true })),
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

describe("NotificationDropdown", () => {
  it("shows bell icon with unread count", async () => {
    renderWithProviders(<NotificationDropdown />)
    await waitFor(() => {
      expect(screen.getByText("2")).toBeInTheDocument()
    })
  })

  it("opens dropdown showing notifications", async () => {
    const user = userEvent.setup()
    renderWithProviders(<NotificationDropdown />)
    await waitFor(() => {
      expect(screen.getByText("2")).toBeInTheDocument()
    })
    await user.click(screen.getByRole("button", { name: /通知/ }))
    expect(screen.getByText("客户到期提醒")).toBeInTheDocument()
    expect(screen.getByText("发货预警")).toBeInTheDocument()
  })

  it("shows mark-all-read button", async () => {
    const user = userEvent.setup()
    renderWithProviders(<NotificationDropdown />)
    await waitFor(() => {
      expect(screen.getByText("2")).toBeInTheDocument()
    })
    await user.click(screen.getByRole("button", { name: /通知/ }))
    expect(screen.getByText("全部标为已读")).toBeInTheDocument()
  })

  it("shows empty state when no notifications", async () => {
    server.use(
      http.get("/api/v1/notifications", () =>
        HttpResponse.json({ items: [], total: 0 }),
      ),
    )
    const user = userEvent.setup()
    renderWithProviders(<NotificationDropdown />)
    await user.click(screen.getByRole("button", { name: /通知/ }))
    await waitFor(() => {
      expect(screen.getByText("暂无通知")).toBeInTheDocument()
    })
  })
})
