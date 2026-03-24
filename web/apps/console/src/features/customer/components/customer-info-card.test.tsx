import { render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"
import { CustomerInfoCard } from "./customer-info-card"
import type { CustomerResponse } from "../types"

const mockCustomer: CustomerResponse = {
  id: "cust-1",
  name: "Acme Corp",
  country: "US",
  region: "California",
  city: "San Francisco",
  address: "123 Main St",
  industry: "electronics",
  source: "alibaba",
  company_size: "50-200",
  website: "https://acme.com",
  main_products: "LED Lights",
  annual_volume: "$500,000",
  current_supplier: "SupplierX",
  decision_process: "Committee",
  custom_fields: { preferred_color: "Blue", payment_terms: "Net 30" },
  grade: { id: "g1", name: "A", color: "#22c55e", position: 1 },
  tags: [],
  contacts: [],
  contact_count: 0,
  last_follow_at: null,
  follow_status: null,
  created_at: "2026-01-01T00:00:00Z",
  updated_at: "2026-01-15T00:00:00Z",
}

describe("CustomerInfoCard", () => {
  it("renders basic info: industry, source, company_size, website", () => {
    render(<CustomerInfoCard customer={mockCustomer} />)

    expect(screen.getByText("基本信息")).toBeInTheDocument()
    expect(screen.getByText("electronics")).toBeInTheDocument()
    expect(screen.getByText("alibaba")).toBeInTheDocument()
    expect(screen.getByText("50-200")).toBeInTheDocument()
    expect(screen.getByText("https://acme.com")).toBeInTheDocument()
  })

  it("renders background info: main_products, annual_volume, current_supplier", () => {
    render(<CustomerInfoCard customer={mockCustomer} />)

    expect(screen.getByText("采购背景")).toBeInTheDocument()
    expect(screen.getByText("LED Lights")).toBeInTheDocument()
    expect(screen.getByText("$500,000")).toBeInTheDocument()
    expect(screen.getByText("SupplierX")).toBeInTheDocument()
    expect(screen.getByText("Committee")).toBeInTheDocument()
  })

  it("renders custom fields from custom_fields dict", () => {
    render(<CustomerInfoCard customer={mockCustomer} />)

    expect(screen.getByText("自定义字段")).toBeInTheDocument()
    expect(screen.getByText("preferred_color")).toBeInTheDocument()
    expect(screen.getByText("Blue")).toBeInTheDocument()
    expect(screen.getByText("payment_terms")).toBeInTheDocument()
    expect(screen.getByText("Net 30")).toBeInTheDocument()
  })
})
