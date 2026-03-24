import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import { CustomerHeader } from "./customer-header"
import type { CustomerResponse } from "../types"

const mockCustomer: CustomerResponse = {
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
  last_follow_at: "2026-01-15T00:00:00Z",
  follow_status: "contacted",
  created_at: "2026-01-01T00:00:00Z",
  updated_at: "2026-01-15T00:00:00Z",
}

describe("CustomerHeader", () => {
  it("renders company name, GradeBadge, and CountryFlag", () => {
    render(
      <CustomerHeader
        customer={mockCustomer}
        onEdit={vi.fn()}
        onDelete={vi.fn()}
      />,
    )

    expect(screen.getByText("Acme Corp")).toBeInTheDocument()
    expect(screen.getByText("A")).toBeInTheDocument()
    expect(screen.getByText("United States")).toBeInTheDocument()
  })

  it("renders tags as colored badges", () => {
    render(
      <CustomerHeader
        customer={mockCustomer}
        onEdit={vi.fn()}
        onDelete={vi.fn()}
      />,
    )

    expect(screen.getByText("VIP")).toBeInTheDocument()
    expect(screen.getByText("Active")).toBeInTheDocument()
  })

  it("dropdown menu has 编辑 and 删除 options", async () => {
    const user = userEvent.setup()
    render(
      <CustomerHeader
        customer={mockCustomer}
        onEdit={vi.fn()}
        onDelete={vi.fn()}
      />,
    )

    await user.click(screen.getByLabelText("Actions"))
    expect(screen.getByText("编辑")).toBeInTheDocument()
    expect(screen.getByText("删除")).toBeInTheDocument()
  })

  it("删除 shows confirmation AlertDialog before calling onDelete", async () => {
    const user = userEvent.setup()
    const onDelete = vi.fn()

    render(
      <CustomerHeader
        customer={mockCustomer}
        onEdit={vi.fn()}
        onDelete={onDelete}
      />,
    )

    await user.click(screen.getByLabelText("Actions"))
    await user.click(screen.getByText("删除"))

    expect(screen.getByText("确认删除客户？")).toBeInTheDocument()
    await user.click(screen.getByText("确认删除"))
    expect(onDelete).toHaveBeenCalledOnce()
  })
})
