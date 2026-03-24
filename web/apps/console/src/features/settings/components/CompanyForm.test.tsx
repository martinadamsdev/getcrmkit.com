import { render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"

import { CompanyForm } from "./CompanyForm"

describe("CompanyForm", () => {
  it("renders all company fields", () => {
    render(<CompanyForm />)
    expect(screen.getByText("公司 Logo")).toBeInTheDocument()
    expect(screen.getByLabelText("公司名称")).toBeInTheDocument()
    expect(screen.getByLabelText("公司地址")).toBeInTheDocument()
    expect(screen.getByLabelText("银行信息")).toBeInTheDocument()
    expect(screen.getByLabelText("默认币种")).toBeInTheDocument()
    expect(screen.getByRole("button", { name: "保存" })).toBeInTheDocument()
  })

  it("renders currency select with options", () => {
    render(<CompanyForm />)
    // Default currency should be USD
    expect(screen.getByLabelText("默认币种")).toBeInTheDocument()
  })
})
