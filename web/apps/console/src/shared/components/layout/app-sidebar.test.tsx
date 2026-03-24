// web/apps/console/src/shared/components/layout/app-sidebar.test.tsx
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { AppSidebar } from "./app-sidebar";
import { SidebarProvider } from "@workspace/ui/components/sidebar";
import { TooltipProvider } from "@workspace/ui/components/tooltip";

// Mock TanStack Router
vi.mock("@tanstack/react-router", async () => {
  const actual = await vi.importActual("@tanstack/react-router");
  return {
    ...actual,
    useRouterState: () => ({ location: { pathname: "/" } }),
    Link: ({ to, children, ...props }: any) => (
      <a href={to} {...props}>{children}</a>
    ),
  };
});

function renderSidebar(badges: Record<string, number> = {}) {
  return render(
    <TooltipProvider>
      <SidebarProvider>
        <AppSidebar badges={badges} />
      </SidebarProvider>
    </TooltipProvider>,
  );
}

describe("AppSidebar", () => {
  it("renders CRMKit brand", () => {
    renderSidebar();
    expect(screen.getByText("CRMKit")).toBeInTheDocument();
  });

  it("renders all navigation items", () => {
    renderSidebar();
    expect(screen.getByText("看板")).toBeInTheDocument();
    expect(screen.getByText("客户")).toBeInTheDocument();
    expect(screen.getByText("跟进")).toBeInTheDocument();
    expect(screen.getByText("产品")).toBeInTheDocument();
    expect(screen.getByText("报价")).toBeInTheDocument();
    expect(screen.getByText("订单")).toBeInTheDocument();
    expect(screen.getByText("设置")).toBeInTheDocument();
  });

  it("renders navigation links with correct hrefs", () => {
    renderSidebar();
    const links = screen.getAllByRole("link");
    const hrefs = links.map((link) => link.getAttribute("href"));
    expect(hrefs).toContain("/");
    expect(hrefs).toContain("/customers");
    expect(hrefs).toContain("/follow-ups");
    expect(hrefs).toContain("/products");
    expect(hrefs).toContain("/quotations");
    expect(hrefs).toContain("/orders");
    expect(hrefs).toContain("/settings");
  });

  it("displays badge counts when provided", () => {
    renderSidebar({
      customers: 5,
      follow_ups: 12,
      quotations: 3,
      orders: 1,
    });
    expect(screen.getByText("5")).toBeInTheDocument();
    expect(screen.getByText("12")).toBeInTheDocument();
    expect(screen.getByText("3")).toBeInTheDocument();
    expect(screen.getByText("1")).toBeInTheDocument();
  });

  it("does not display badge when count is 0", () => {
    renderSidebar({ customers: 0 });
    // 0 should not render a badge element
    const badges = screen.queryAllByText("0");
    // Filter to only sidebar badge elements (not other "0" text)
    expect(badges).toHaveLength(0);
  });
});
