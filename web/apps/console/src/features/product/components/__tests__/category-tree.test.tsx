import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import { CategoryTree } from "../category-tree"

const MOCK_CATEGORIES = [
  {
    id: "cat-1",
    name: "电子产品",
    parent_id: null,
    level: 1,
    position: 0,
    product_count: 15,
    children: [
      {
        id: "cat-2",
        name: "手机配件",
        parent_id: "cat-1",
        level: 2,
        position: 0,
        product_count: 8,
        children: [
          {
            id: "cat-3",
            name: "手机壳",
            parent_id: "cat-2",
            level: 3,
            position: 0,
            product_count: 5,
            children: [],
          },
        ],
      },
    ],
  },
  {
    id: "cat-4",
    name: "服装",
    parent_id: null,
    level: 1,
    position: 1,
    product_count: 20,
    children: [],
  },
]

describe("CategoryTree", () => {
  it("renders top-level categories", () => {
    render(
      <CategoryTree
        categories={MOCK_CATEGORIES}
        selectedId={null}
        onSelect={() => {}}
        onReorder={() => {}}
      />,
    )
    expect(screen.getByText("电子产品")).toBeInTheDocument()
    expect(screen.getByText("服装")).toBeInTheDocument()
  })

  it("shows product count badges", () => {
    render(
      <CategoryTree
        categories={MOCK_CATEGORIES}
        selectedId={null}
        onSelect={() => {}}
        onReorder={() => {}}
      />,
    )
    expect(screen.getByText("15")).toBeInTheDocument()
    expect(screen.getByText("20")).toBeInTheDocument()
  })

  it("expands child categories on click", async () => {
    const user = userEvent.setup()
    render(
      <CategoryTree
        categories={MOCK_CATEGORIES}
        selectedId={null}
        onSelect={() => {}}
        onReorder={() => {}}
      />,
    )
    await user.click(screen.getByText("电子产品"))
    expect(screen.getByText("手机配件")).toBeInTheDocument()
  })

  it("calls onSelect when category clicked", async () => {
    const user = userEvent.setup()
    const onSelect = vi.fn()
    render(
      <CategoryTree
        categories={MOCK_CATEGORIES}
        selectedId={null}
        onSelect={onSelect}
        onReorder={() => {}}
      />,
    )
    await user.click(screen.getByText("服装"))
    expect(onSelect).toHaveBeenCalledWith("cat-4")
  })

  it("highlights selected category", () => {
    render(
      <CategoryTree
        categories={MOCK_CATEGORIES}
        selectedId="cat-4"
        onSelect={() => {}}
        onReorder={() => {}}
      />,
    )
    const item = screen.getByText("服装").closest("[data-selected]")
    expect(item).toHaveAttribute("data-selected", "true")
  })

  it("renders empty state when no categories", () => {
    render(
      <CategoryTree
        categories={[]}
        selectedId={null}
        onSelect={() => {}}
        onReorder={() => {}}
      />,
    )
    expect(screen.getByText("暂无分类")).toBeInTheDocument()
  })
})
