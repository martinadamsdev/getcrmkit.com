import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it } from "vitest"

import { ProfileForm } from "./ProfileForm"

describe("ProfileForm", () => {
  it("renders all profile fields", () => {
    render(<ProfileForm />)
    expect(screen.getByText("头像")).toBeInTheDocument()
    expect(screen.getByLabelText("姓名")).toBeInTheDocument()
    expect(screen.getByLabelText("邮箱")).toBeInTheDocument()
    expect(screen.getByLabelText("时区")).toBeInTheDocument()
    expect(screen.getByRole("button", { name: "修改密码" })).toBeInTheDocument()
    expect(screen.getByRole("button", { name: "保存" })).toBeInTheDocument()
  })

  it("shows password change fields when clicking change password", async () => {
    const user = userEvent.setup()
    render(<ProfileForm />)
    await user.click(screen.getByRole("button", { name: "修改密码" }))
    expect(screen.getByLabelText("当前密码")).toBeInTheDocument()
    expect(screen.getByLabelText("新密码")).toBeInTheDocument()
    expect(screen.getByLabelText("确认密码")).toBeInTheDocument()
  })

  it("hides password change fields when toggling off", async () => {
    const user = userEvent.setup()
    render(<ProfileForm />)
    await user.click(screen.getByRole("button", { name: "修改密码" }))
    expect(screen.getByLabelText("当前密码")).toBeInTheDocument()
    await user.click(screen.getByRole("button", { name: "取消修改密码" }))
    expect(screen.queryByLabelText("当前密码")).not.toBeInTheDocument()
  })
})
