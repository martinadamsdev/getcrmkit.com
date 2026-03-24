import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"

import { DynamicField } from "./DynamicField"

describe("DynamicField", () => {
  it("renders text input for text type", () => {
    const onChange = vi.fn()
    render(
      <DynamicField
        definition={{ id: "f1", name: "备注", type: "text", required: false, options: [] }}
        value=""
        onChange={onChange}
      />,
    )
    expect(screen.getByLabelText("备注")).toBeInTheDocument()
    expect(screen.getByRole("textbox")).toBeInTheDocument()
  })

  it("renders number input for number type", () => {
    const onChange = vi.fn()
    render(
      <DynamicField
        definition={{ id: "f2", name: "数量", type: "number", required: false, options: [] }}
        value={0}
        onChange={onChange}
      />,
    )
    expect(screen.getByLabelText("数量")).toBeInTheDocument()
    expect(screen.getByRole("spinbutton")).toBeInTheDocument()
  })

  it("renders date picker for date type", () => {
    const onChange = vi.fn()
    render(
      <DynamicField
        definition={{ id: "f3", name: "到期日", type: "date", required: false, options: [] }}
        value=""
        onChange={onChange}
      />,
    )
    expect(screen.getByLabelText("到期日")).toBeInTheDocument()
  })

  it("renders select for select type with options", () => {
    const onChange = vi.fn()
    render(
      <DynamicField
        definition={{
          id: "f4",
          name: "来源",
          type: "select",
          required: false,
          options: ["阿里巴巴", "展会", "官网"],
        }}
        value=""
        onChange={onChange}
      />,
    )
    expect(screen.getByLabelText("来源")).toBeInTheDocument()
  })

  it("renders switch for boolean type", () => {
    const onChange = vi.fn()
    render(
      <DynamicField
        definition={{ id: "f5", name: "VIP", type: "boolean", required: false, options: [] }}
        value={false}
        onChange={onChange}
      />,
    )
    expect(screen.getByLabelText("VIP")).toBeInTheDocument()
    expect(screen.getByRole("switch")).toBeInTheDocument()
  })

  it("shows required indicator when required", () => {
    const onChange = vi.fn()
    render(
      <DynamicField
        definition={{ id: "f6", name: "必填字段", type: "text", required: true, options: [] }}
        value=""
        onChange={onChange}
      />,
    )
    expect(screen.getByText("*")).toBeInTheDocument()
  })

  it("calls onChange on text input", async () => {
    const onChange = vi.fn()
    const user = userEvent.setup()
    render(
      <DynamicField
        definition={{ id: "f1", name: "备注", type: "text", required: false, options: [] }}
        value=""
        onChange={onChange}
      />,
    )
    await user.type(screen.getByRole("textbox"), "hello")
    expect(onChange).toHaveBeenCalled()
  })
})
