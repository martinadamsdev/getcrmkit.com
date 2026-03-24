import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, it, expect, vi } from "vitest"
import { Inbox } from "lucide-react"
import { EmptyState } from "./empty-state"

describe("EmptyState", () => {
  it("renders icon, title, and description", () => {
    render(
      <EmptyState
        icon={Inbox}
        title="No data"
        description="Nothing to show here"
      />,
    )
    expect(screen.getByText("No data")).toBeInTheDocument()
    expect(screen.getByText("Nothing to show here")).toBeInTheDocument()
  })

  it("renders action button when action prop provided", () => {
    render(
      <EmptyState
        icon={Inbox}
        title="No data"
        action={{ label: "Create new", onClick: vi.fn() }}
      />,
    )
    expect(screen.getByRole("button", { name: "Create new" })).toBeInTheDocument()
  })

  it("calls action.onClick when button clicked", async () => {
    const user = userEvent.setup()
    const onClick = vi.fn()
    render(
      <EmptyState
        icon={Inbox}
        title="No data"
        action={{ label: "Create new", onClick }}
      />,
    )
    await user.click(screen.getByRole("button", { name: "Create new" }))
    expect(onClick).toHaveBeenCalledOnce()
  })
})
