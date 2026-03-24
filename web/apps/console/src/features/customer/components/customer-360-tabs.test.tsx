import { render, screen, within } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it } from "vitest"
import { Customer360Tabs } from "./customer-360-tabs"
import type { Customer360Response } from "../types"

const mock360Data: Customer360Response = {
  customer: {
    id: "cust-1",
    name: "Acme Corp",
    country: "US",
    industry: "electronics",
    source: "alibaba",
    company_size: "50-200",
    website: "https://acme.com",
    grade: { id: "g1", name: "A", color: "#22c55e", position: 1 },
    tags: [],
    contacts: [
      {
        id: "ct-1",
        customer_id: "cust-1",
        name: "John Smith",
        title: "Manager",
        email: "john@acme.com",
        phone: null,
        whatsapp: null,
        skype: null,
        linkedin: null,
        wechat: null,
        is_primary: true,
        notes: null,
        created_at: "2026-01-01T00:00:00Z",
        updated_at: "2026-01-01T00:00:00Z",
      },
    ],
    contact_count: 3,
    last_follow_at: null,
    follow_status: null,
    created_at: "2026-01-01T00:00:00Z",
    updated_at: "2026-01-15T00:00:00Z",
  },
  stats: {
    contact_count: 3,
    follow_up_count: 12,
    quotation_count: 5,
    order_count: 2,
  },
  recent_follow_ups: [],
  quotations: [],
}

describe("Customer360Tabs", () => {
  it("renders 5 tabs: 基本信息, 联系人, 跟进记录, 报价, 订单", () => {
    render(<Customer360Tabs data={mock360Data} />)

    const tabList = screen.getByRole("tablist")
    const tabs = within(tabList).getAllByRole("tab")
    expect(tabs).toHaveLength(5)

    expect(within(tabList).getByRole("tab", { name: /基本信息/ })).toBeInTheDocument()
    expect(within(tabList).getByRole("tab", { name: /联系人/ })).toBeInTheDocument()
    expect(within(tabList).getByRole("tab", { name: /跟进记录/ })).toBeInTheDocument()
    expect(within(tabList).getByRole("tab", { name: /报价/ })).toBeInTheDocument()
    expect(within(tabList).getByRole("tab", { name: /订单/ })).toBeInTheDocument()
  })

  it("shows count badges on tabs with non-zero counts", () => {
    render(<Customer360Tabs data={mock360Data} />)

    const tabList = screen.getByRole("tablist")
    expect(within(tabList).getByText("3")).toBeInTheDocument()
    expect(within(tabList).getByText("12")).toBeInTheDocument()
    expect(within(tabList).getByText("5")).toBeInTheDocument()
    expect(within(tabList).getByText("2")).toBeInTheDocument()
  })

  it("switches tab content when tab clicked", async () => {
    const user = userEvent.setup()
    render(<Customer360Tabs data={mock360Data} />)

    const tabList = screen.getByRole("tablist")

    // Click on contacts tab
    await user.click(within(tabList).getByRole("tab", { name: /联系人/ }))
    expect(screen.getByText("John Smith")).toBeInTheDocument()
  })
})
