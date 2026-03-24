import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import { CustomerCreateDialog } from "./customer-create-dialog"
import type { DuplicateMatch } from "../types"

describe("CustomerCreateDialog", () => {
  const defaultProps = {
    open: true,
    onOpenChange: vi.fn(),
    onSubmit: vi.fn(),
    onCheckDuplicate: vi.fn().mockResolvedValue([]),
    onViewExisting: vi.fn(),
  }

  it("renders form fields: 公司名(required), 国家, 行业, 来源, 网站", () => {
    render(<CustomerCreateDialog {...defaultProps} />)

    expect(screen.getByText("新建客户")).toBeInTheDocument()
    expect(screen.getByLabelText(/公司名/)).toBeInTheDocument()
    expect(screen.getByText("国家")).toBeInTheDocument()
    expect(screen.getByText("行业")).toBeInTheDocument()
    expect(screen.getByText("来源")).toBeInTheDocument()
    expect(screen.getByText("网站")).toBeInTheDocument()
  })

  it("submit button disabled when 公司名 is empty", () => {
    render(<CustomerCreateDialog {...defaultProps} />)

    const submitButton = screen.getByRole("button", { name: "创建" })
    expect(submitButton).toBeDisabled()
  })

  it("debounce 500ms after typing company name calls onCheckDuplicate", async () => {
    const onCheckDuplicate = vi.fn().mockResolvedValue([])

    render(
      <CustomerCreateDialog
        {...defaultProps}
        onCheckDuplicate={onCheckDuplicate}
      />,
    )

    await userEvent.type(screen.getByLabelText(/公司名/), "Acme")

    await waitFor(() => {
      expect(onCheckDuplicate).toHaveBeenCalledWith("Acme")
    }, { timeout: 1500 })
  })

  it("shows DuplicateWarningDialog when duplicates found", async () => {
    const duplicates: DuplicateMatch[] = [
      {
        customer_id: "c1",
        customer_name: "Acme Corp",
        match_type: "company_name",
        matched_value: "Acme Corp",
      },
    ]
    const onCheckDuplicate = vi.fn().mockResolvedValue(duplicates)

    render(
      <CustomerCreateDialog
        {...defaultProps}
        onCheckDuplicate={onCheckDuplicate}
      />,
    )

    await userEvent.type(screen.getByLabelText(/公司名/), "Acme")

    await waitFor(() => {
      expect(screen.getByText("发现疑似重复客户")).toBeInTheDocument()
    }, { timeout: 1500 })
  })

  it("on successful submit calls onSubmit with form data", async () => {
    const onSubmit = vi.fn()

    render(
      <CustomerCreateDialog
        {...defaultProps}
        onSubmit={onSubmit}
      />,
    )

    await userEvent.type(screen.getByLabelText(/公司名/), "NewCorp")

    // Wait for debounce to settle
    await waitFor(() => {
      expect(screen.getByRole("button", { name: "创建" })).not.toBeDisabled()
    }, { timeout: 1500 })

    await userEvent.click(screen.getByRole("button", { name: "创建" }))

    expect(onSubmit).toHaveBeenCalledWith(
      expect.objectContaining({ name: "NewCorp" }),
    )
  })

  it("on '忽略并继续创建' in duplicate dialog proceeds to submit", async () => {
    const duplicates: DuplicateMatch[] = [
      {
        customer_id: "c1",
        customer_name: "Acme Corp",
        match_type: "company_name",
        matched_value: "Acme Corp",
      },
    ]
    const onCheckDuplicate = vi.fn().mockResolvedValue(duplicates)
    const onSubmit = vi.fn()

    render(
      <CustomerCreateDialog
        {...defaultProps}
        onCheckDuplicate={onCheckDuplicate}
        onSubmit={onSubmit}
      />,
    )

    await userEvent.type(screen.getByLabelText(/公司名/), "Acme")

    await waitFor(() => {
      expect(screen.getByText("发现疑似重复客户")).toBeInTheDocument()
    }, { timeout: 1500 })

    await userEvent.click(screen.getByRole("button", { name: "忽略并继续创建" }))

    expect(onSubmit).toHaveBeenCalledWith(
      expect.objectContaining({ name: "Acme" }),
    )
  })
})
