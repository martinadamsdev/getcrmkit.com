import { render, screen } from "@testing-library/react"
import { describe, expect, it, vi } from "vitest"

import { SettingsSidebar } from "./SettingsSidebar"

vi.mock("@tanstack/react-router", () => ({
  Link: ({ children, to, ...props }: any) => (
    <a href={to} {...props}>{children}</a>
  ),
  useMatchRoute: () => () => false,
}))

describe("SettingsSidebar", () => {
  it("renders all 4 navigation items", () => {
    render(<SettingsSidebar />)
    expect(screen.getByText("个人信息")).toBeInTheDocument()
    expect(screen.getByText("公司信息")).toBeInTheDocument()
    expect(screen.getByText("话术模板")).toBeInTheDocument()
    expect(screen.getByText("自定义字段")).toBeInTheDocument()
  })

  it("renders correct links", () => {
    render(<SettingsSidebar />)
    const links = screen.getAllByRole("link")
    expect(links).toHaveLength(4)
    expect(links[0]).toHaveAttribute("href", "/settings/profile")
    expect(links[1]).toHaveAttribute("href", "/settings/company")
    expect(links[2]).toHaveAttribute("href", "/settings/templates")
    expect(links[3]).toHaveAttribute("href", "/settings/custom-fields")
  })
})
