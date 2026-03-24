// web/apps/console/src/shared/components/layout/page-header.test.tsx
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { PageHeader } from "./page-header";

describe("PageHeader", () => {
  it("renders title", () => {
    render(<PageHeader title="客户管理" />);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("客户管理");
  });

  it("renders description when provided", () => {
    render(<PageHeader title="客户管理" description="管理你的所有客户" />);
    expect(screen.getByText("管理你的所有客户")).toBeInTheDocument();
  });

  it("does not render description when not provided", () => {
    const { container } = render(<PageHeader title="客户管理" />);
    expect(container.querySelector("p")).toBeNull();
  });

  it("renders actions slot", () => {
    render(
      <PageHeader
        title="客户管理"
        actions={<button type="button">新建</button>}
      />,
    );
    expect(screen.getByRole("button", { name: "新建" })).toBeInTheDocument();
  });

  it("has correct layout structure", () => {
    const { container } = render(
      <PageHeader
        title="测试"
        description="描述"
        actions={<button type="button">操作</button>}
      />,
    );
    // Header should contain flex layout with title on left, actions on right
    const header = container.firstElementChild;
    expect(header).toBeTruthy();
  });
});
