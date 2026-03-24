import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import { CustomerTable } from "./customer-table"
import type { CustomerResponse } from "../types"

const mockCustomers: CustomerResponse[] = [
  {
    id: "cust-1",
    name: "Acme Corp",
    country: "US",
    industry: "electronics",
    source: "alibaba",
    company_size: "50-200",
    website: "https://acme.com",
    grade: { id: "g1", name: "A", color: "#22c55e", position: 1 },
    tags: [
      { id: "t1", name: "VIP", color: "#ef4444" },
      { id: "t2", name: "Active", color: "#3b82f6" },
    ],
    contacts: [],
    contact_count: 3,
    last_follow_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
    follow_status: "contacted",
    created_at: "2026-01-01T00:00:00Z",
    updated_at: "2026-01-15T00:00:00Z",
  },
  {
    id: "cust-2",
    name: "Globex Ltd",
    country: "GB",
    industry: "textiles",
    source: "exhibition",
    company_size: "200-500",
    website: null,
    grade: { id: "g2", name: "B", color: "#3b82f6", position: 2 },
    tags: [],
    contacts: [],
    contact_count: 1,
    last_follow_at: null,
    follow_status: "new",
    created_at: "2026-02-01T00:00:00Z",
    updated_at: "2026-02-10T00:00:00Z",
  },
]

describe("CustomerTable", () => {
  const defaultProps = {
    data: mockCustomers,
    pagination: { page: 1, pageSize: 20, total: 2 },
    onPageChange: vi.fn(),
  }

  it("renders column headers: 公司名, 国家, 等级, 标签, 来源, 最近跟进, 联系人数", () => {
    render(<CustomerTable {...defaultProps} />)

    expect(screen.getByText("公司名")).toBeInTheDocument()
    expect(screen.getByText("国家")).toBeInTheDocument()
    expect(screen.getByText("等级")).toBeInTheDocument()
    expect(screen.getByText("标签")).toBeInTheDocument()
    expect(screen.getByText("来源")).toBeInTheDocument()
    expect(screen.getByText("最近跟进")).toBeInTheDocument()
    expect(screen.getByText("联系人数")).toBeInTheDocument()
  })

  it("renders customer rows with GradeBadge and CountryFlag", () => {
    render(<CustomerTable {...defaultProps} />)

    expect(screen.getByText("Acme Corp")).toBeInTheDocument()
    expect(screen.getByText("Globex Ltd")).toBeInTheDocument()
    // GradeBadge renders grade letter
    expect(screen.getByText("A")).toBeInTheDocument()
    expect(screen.getByText("B")).toBeInTheDocument()
  })

  it("calls onRowClick when a row is clicked", async () => {
    const user = userEvent.setup()
    const onRowClick = vi.fn()

    render(<CustomerTable {...defaultProps} onRowClick={onRowClick} />)

    await user.click(screen.getByText("Acme Corp"))
    expect(onRowClick).toHaveBeenCalledWith(
      expect.objectContaining({ id: "cust-1" }),
    )
  })

  it("shows tags as colored badges", () => {
    render(<CustomerTable {...defaultProps} />)

    expect(screen.getByText("VIP")).toBeInTheDocument()
    expect(screen.getByText("Active")).toBeInTheDocument()
  })

  it("shows relative time for last_follow_at and '—' when null", () => {
    render(<CustomerTable {...defaultProps} />)

    // Acme Corp has last_follow_at 3 days ago
    expect(screen.getByText("3 天前")).toBeInTheDocument()
    // Globex Ltd has null last_follow_at - check for dash
    const dashElements = screen.getAllByText("—")
    expect(dashElements.length).toBeGreaterThanOrEqual(1)
  })
})
