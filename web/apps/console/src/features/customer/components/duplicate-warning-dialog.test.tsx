import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import { DuplicateWarningDialog } from "./duplicate-warning-dialog"
import type { DuplicateMatch } from "../types"

const mockDuplicates: DuplicateMatch[] = [
  {
    customer_id: "cust-1",
    customer_name: "Acme Corp",
    match_type: "company_name",
    matched_value: "Acme Corp",
  },
  {
    customer_id: "cust-2",
    customer_name: "Acme Inc",
    match_type: "website",
    matched_value: "acme.com",
  },
]

describe("DuplicateWarningDialog", () => {
  it("renders title and duplicate matches", () => {
    render(
      <DuplicateWarningDialog
        open={true}
        onOpenChange={vi.fn()}
        duplicates={mockDuplicates}
        onIgnore={vi.fn()}
        onViewExisting={vi.fn()}
      />,
    )

    expect(screen.getByText("发现疑似重复客户")).toBeInTheDocument()
    // Customer names rendered as buttons
    expect(screen.getByRole("button", { name: "Acme Corp" })).toBeInTheDocument()
    expect(screen.getByRole("button", { name: "Acme Inc" })).toBeInTheDocument()
    expect(screen.getByText("company_name")).toBeInTheDocument()
    expect(screen.getByText("website")).toBeInTheDocument()
    expect(screen.getByText("acme.com")).toBeInTheDocument()
  })

  it("calls onIgnore when '忽略并继续创建' button clicked", async () => {
    const user = userEvent.setup()
    const onIgnore = vi.fn()

    render(
      <DuplicateWarningDialog
        open={true}
        onOpenChange={vi.fn()}
        duplicates={mockDuplicates}
        onIgnore={onIgnore}
        onViewExisting={vi.fn()}
      />,
    )

    await user.click(screen.getByRole("button", { name: "忽略并继续创建" }))
    expect(onIgnore).toHaveBeenCalledOnce()
  })

  it("calls onViewExisting with customer_id when customer name clicked", async () => {
    const user = userEvent.setup()
    const onViewExisting = vi.fn()

    render(
      <DuplicateWarningDialog
        open={true}
        onOpenChange={vi.fn()}
        duplicates={mockDuplicates}
        onIgnore={vi.fn()}
        onViewExisting={onViewExisting}
      />,
    )

    await user.click(screen.getByRole("button", { name: "Acme Corp" }))
    expect(onViewExisting).toHaveBeenCalledWith("cust-1")
  })
})
