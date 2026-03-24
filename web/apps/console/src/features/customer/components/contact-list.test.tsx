import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import { ContactList } from "./contact-list"
import type { ContactResponse } from "../types"

const mockContacts: ContactResponse[] = [
  {
    id: "ct-1",
    customer_id: "cust-1",
    name: "John Smith",
    title: "Purchasing Manager",
    email: "john@acme.com",
    phone: "+1234567890",
    whatsapp: "+1234567890",
    skype: "john.smith",
    linkedin: "https://linkedin.com/in/john",
    wechat: null,
    is_primary: true,
    notes: null,
    created_at: "2026-01-01T00:00:00Z",
    updated_at: "2026-01-15T00:00:00Z",
  },
  {
    id: "ct-2",
    customer_id: "cust-1",
    name: "Jane Doe",
    title: "Sales Director",
    email: "jane@acme.com",
    phone: null,
    whatsapp: null,
    skype: null,
    linkedin: null,
    wechat: "jane_doe_wx",
    is_primary: false,
    notes: null,
    created_at: "2026-02-01T00:00:00Z",
    updated_at: "2026-02-10T00:00:00Z",
  },
]

describe("ContactList", () => {
  it("renders list of contacts with name, title, and primary badge", () => {
    render(<ContactList customerId="cust-1" contacts={mockContacts} />)

    expect(screen.getByText("John Smith")).toBeInTheDocument()
    expect(screen.getByText("Purchasing Manager")).toBeInTheDocument()
    expect(screen.getByText("主要联系人")).toBeInTheDocument()

    expect(screen.getByText("Jane Doe")).toBeInTheDocument()
    expect(screen.getByText("Sales Director")).toBeInTheDocument()
  })

  it("shows communication channel icons for contacts", () => {
    render(<ContactList customerId="cust-1" contacts={mockContacts} />)

    // John has email, phone, whatsapp, skype, linkedin
    expect(screen.getByLabelText("email: john@acme.com")).toBeInTheDocument()
    expect(screen.getByLabelText("phone: +1234567890")).toBeInTheDocument()
    expect(screen.getByLabelText("whatsapp: +1234567890")).toBeInTheDocument()
    expect(screen.getByLabelText("skype: john.smith")).toBeInTheDocument()
    expect(
      screen.getByLabelText("linkedin: https://linkedin.com/in/john"),
    ).toBeInTheDocument()

    // Jane has email and wechat
    expect(screen.getByLabelText("email: jane@acme.com")).toBeInTheDocument()
    expect(screen.getByLabelText("wechat: jane_doe_wx")).toBeInTheDocument()
  })

  it("primary contact shows star indicator", () => {
    render(<ContactList customerId="cust-1" contacts={mockContacts} />)

    expect(screen.getByText("主要联系人")).toBeInTheDocument()
    expect(screen.getAllByText("主要联系人")).toHaveLength(1)
  })

  it("shows '添加联系人' button at the bottom", () => {
    render(<ContactList customerId="cust-1" contacts={mockContacts} />)

    // The button at bottom contains "添加联系人"
    const buttons = screen.getAllByRole("button", { name: /添加联系人/ })
    expect(buttons.length).toBeGreaterThanOrEqual(1)
  })

  it("opens ContactCreateDialog when bottom '添加联系人' button clicked", async () => {
    const user = userEvent.setup()
    render(<ContactList customerId="cust-1" contacts={mockContacts} />)

    // Click the bottom "添加联系人" button
    const addButtons = screen.getAllByRole("button", { name: /添加联系人/ })
    await user.click(addButtons[addButtons.length - 1])

    // Dialog should appear with title
    expect(screen.getByRole("heading", { name: "添加联系人" })).toBeInTheDocument()
  })
})
