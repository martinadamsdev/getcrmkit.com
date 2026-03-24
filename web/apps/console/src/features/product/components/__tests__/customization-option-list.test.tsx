import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import { CustomizationOptionList } from "../customization-option-list"

const MOCK_OPTIONS = [
  { id: "opt-1", name: "Logo 印刷", surcharge: "5.00" },
  { id: "opt-2", name: "定制包装", surcharge: "3.50" },
]

describe("CustomizationOptionList", () => {
  it("renders option names", () => {
    render(
      <CustomizationOptionList
        options={MOCK_OPTIONS}
        onAdd={() => {}}
        onUpdate={() => {}}
        onDelete={() => {}}
      />,
    )
    expect(screen.getByDisplayValue("Logo 印刷")).toBeInTheDocument()
    expect(screen.getByDisplayValue("定制包装")).toBeInTheDocument()
  })

  it("renders surcharge values", () => {
    render(
      <CustomizationOptionList
        options={MOCK_OPTIONS}
        onAdd={() => {}}
        onUpdate={() => {}}
        onDelete={() => {}}
      />,
    )
    expect(screen.getByDisplayValue("5.00")).toBeInTheDocument()
    expect(screen.getByDisplayValue("3.50")).toBeInTheDocument()
  })

  it("renders add option button", () => {
    render(
      <CustomizationOptionList
        options={MOCK_OPTIONS}
        onAdd={() => {}}
        onUpdate={() => {}}
        onDelete={() => {}}
      />,
    )
    expect(
      screen.getByRole("button", { name: /添加选项/ }),
    ).toBeInTheDocument()
  })

  it("calls onAdd when add button clicked", async () => {
    const user = userEvent.setup()
    const onAdd = vi.fn()
    render(
      <CustomizationOptionList
        options={MOCK_OPTIONS}
        onAdd={onAdd}
        onUpdate={() => {}}
        onDelete={() => {}}
      />,
    )
    await user.click(screen.getByRole("button", { name: /添加选项/ }))
    expect(onAdd).toHaveBeenCalledOnce()
  })

  it("renders empty state", () => {
    render(
      <CustomizationOptionList
        options={[]}
        onAdd={() => {}}
        onUpdate={() => {}}
        onDelete={() => {}}
      />,
    )
    expect(screen.getByText(/暂无定制选项/)).toBeInTheDocument()
  })
})
