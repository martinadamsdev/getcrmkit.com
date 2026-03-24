import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, it, expect, vi } from "vitest"
import { type ColumnDef } from "@tanstack/react-table"
import { DataTable } from "./data-table"

type TestRow = { id: string; name: string; email: string }

const columns: ColumnDef<TestRow>[] = [
  { accessorKey: "name", header: "Name" },
  { accessorKey: "email", header: "Email" },
]

const data: TestRow[] = [
  { id: "1", name: "Alice", email: "alice@test.com" },
  { id: "2", name: "Bob", email: "bob@test.com" },
]

describe("DataTable", () => {
  it("renders column headers from column definitions", () => {
    render(<DataTable columns={columns} data={data} />)
    expect(screen.getByText("Name")).toBeInTheDocument()
    expect(screen.getByText("Email")).toBeInTheDocument()
  })

  it("renders rows from data array", () => {
    render(<DataTable columns={columns} data={data} />)
    expect(screen.getByText("Alice")).toBeInTheDocument()
    expect(screen.getByText("Bob")).toBeInTheDocument()
    expect(screen.getByText("alice@test.com")).toBeInTheDocument()
  })

  it("calls onRowClick with row data when row clicked", async () => {
    const user = userEvent.setup()
    const onRowClick = vi.fn()
    render(<DataTable columns={columns} data={data} onRowClick={onRowClick} />)
    await user.click(screen.getByText("Alice"))
    expect(onRowClick).toHaveBeenCalledWith(
      expect.objectContaining({ name: "Alice" }),
    )
  })

  it("shows EmptyState when data is empty", () => {
    render(
      <DataTable
        columns={columns}
        data={[]}
        emptyState={{
          title: "No customers",
          description: "Create your first customer",
        }}
      />,
    )
    expect(screen.getByText("No customers")).toBeInTheDocument()
    expect(screen.getByText("Create your first customer")).toBeInTheDocument()
  })

  it("renders pagination controls", () => {
    render(
      <DataTable
        columns={columns}
        data={data}
        pagination={{ page: 1, pageSize: 20, total: 50 }}
        onPageChange={vi.fn()}
      />,
    )
    expect(screen.getByText(/1/)).toBeInTheDocument()
    expect(screen.getByText(/3/)).toBeInTheDocument() // total pages
  })

  it("calls onPageChange when next clicked", async () => {
    const user = userEvent.setup()
    const onPageChange = vi.fn()
    render(
      <DataTable
        columns={columns}
        data={data}
        pagination={{ page: 1, pageSize: 20, total: 50 }}
        onPageChange={onPageChange}
      />,
    )
    await user.click(screen.getByLabelText(/next/i))
    expect(onPageChange).toHaveBeenCalledWith(2)
  })

  it("applies sorting indicator on sortable columns", () => {
    render(
      <DataTable
        columns={columns}
        data={data}
        sorting={[{ id: "name", desc: false }]}
        onSortingChange={vi.fn()}
      />,
    )
    // Column header should show sort direction indicator
    const nameHeader = screen.getByText("Name")
    expect(nameHeader.closest("[data-slot='table-head']")).toBeInTheDocument()
  })

  it("renders loading skeleton when isLoading", () => {
    render(<DataTable columns={columns} data={[]} isLoading />)
    const skeletons = document.querySelectorAll('[data-slot="skeleton"]')
    expect(skeletons.length).toBeGreaterThan(0)
  })
})
