import { render, screen, act } from "@testing-library/react"
import { describe, expect, it, beforeEach } from "vitest"

import { I18nProvider, useI18n } from "./context"
import { useUIStore } from "../stores/ui.store"

function TestConsumer() {
  const { locale, t } = useI18n()
  return (
    <div>
      <span data-testid="locale">{locale}</span>
      <span data-testid="nav">{t("nav_customers")}</span>
      <span data-testid="param">{t("dashboard_days_not_followed", { count: 5 })}</span>
    </div>
  )
}

describe("I18nProvider", () => {
  beforeEach(() => {
    useUIStore.setState({ locale: "zh" })
  })

  it("provides Chinese translations by default", () => {
    render(
      <I18nProvider>
        <TestConsumer />
      </I18nProvider>,
    )
    expect(screen.getByTestId("locale")).toHaveTextContent("zh")
    expect(screen.getByTestId("nav")).toHaveTextContent("客户")
  })

  it("interpolates params", () => {
    render(
      <I18nProvider>
        <TestConsumer />
      </I18nProvider>,
    )
    expect(screen.getByTestId("param")).toHaveTextContent("5天未跟进")
  })

  it("switches to English", () => {
    act(() => {
      useUIStore.setState({ locale: "en" })
    })
    render(
      <I18nProvider>
        <TestConsumer />
      </I18nProvider>,
    )
    expect(screen.getByTestId("locale")).toHaveTextContent("en")
    expect(screen.getByTestId("nav")).toHaveTextContent("Customers")
  })
})
