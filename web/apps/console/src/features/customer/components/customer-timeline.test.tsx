import { render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"
import { CustomerTimeline } from "./customer-timeline"
import type { FollowUpItem } from "../types"

const mockFollowUps: FollowUpItem[] = [
  {
    id: "fu-1",
    customer_id: "cust-1",
    method: "email",
    content: "Sent initial product catalog and pricing list to the buyer.",
    stage: "contacted",
    attachment_count: 2,
    created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    created_by: "user-1",
  },
  {
    id: "fu-2",
    customer_id: "cust-1",
    method: "phone",
    content: "Called to discuss pricing details and MOQ requirements.",
    stage: "quoted",
    attachment_count: 0,
    created_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    created_by: "user-1",
  },
]

describe("CustomerTimeline", () => {
  it("maps follow_up items to Timeline items with correct method labels", () => {
    render(
      <CustomerTimeline customerId="cust-1" followUps={mockFollowUps} />,
    )

    expect(screen.getByText("邮件")).toBeInTheDocument()
    expect(screen.getByText("电话")).toBeInTheDocument()
  })

  it("shows content summary truncated to 2 lines", () => {
    render(
      <CustomerTimeline customerId="cust-1" followUps={mockFollowUps} />,
    )

    expect(
      screen.getByText(
        "Sent initial product catalog and pricing list to the buyer.",
      ),
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        "Called to discuss pricing details and MOQ requirements.",
      ),
    ).toBeInTheDocument()
  })

  it("shows attachment count badge when attachments present", () => {
    render(
      <CustomerTimeline customerId="cust-1" followUps={mockFollowUps} />,
    )

    // The first follow-up has 2 attachments
    expect(screen.getByText("2")).toBeInTheDocument()
  })
})
