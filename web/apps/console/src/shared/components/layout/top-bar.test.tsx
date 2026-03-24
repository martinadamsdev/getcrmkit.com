// web/apps/console/src/shared/components/layout/top-bar.test.tsx
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { TopBar } from "./top-bar";
import { SidebarProvider } from "@workspace/ui/components/sidebar";

// Mock TanStack Router
vi.mock("@tanstack/react-router", async () => {
  const actual = await vi.importActual("@tanstack/react-router");
  return {
    ...actual,
    Link: ({ to, children, ...props }: any) => (
      <a href={to} {...props}>{children}</a>
    ),
  };
});

// Mock useUIStore
vi.mock("@/shared/stores/ui.store", () => ({
  useUIStore: (selector?: any) => {
    const state = {
      theme: "light",
      locale: "zh",
      setTheme: vi.fn(),
      setLocale: vi.fn(),
    };
    return selector ? selector(state) : state;
  },
}));

// Mock NotificationDropdown to avoid react-query dependency
vi.mock("./NotificationDropdown", () => ({
  NotificationDropdown: () => (
    <button type="button" aria-label="通知">Bell</button>
  ),
}));

function renderTopBar(breadcrumbs: Array<{ label: string; href?: string }> = []) {
  return render(
    <SidebarProvider>
      <TopBar breadcrumbs={breadcrumbs} />
    </SidebarProvider>,
  );
}

describe("TopBar", () => {
  it("renders breadcrumbs", () => {
    renderTopBar([
      { label: "首页", href: "/" },
      { label: "客户", href: "/customers" },
    ]);
    expect(screen.getByText("首页")).toBeInTheDocument();
    expect(screen.getByText("客户")).toBeInTheDocument();
  });

  it("renders search trigger with ⌘K hint", () => {
    renderTopBar();
    expect(screen.getByText("搜索...")).toBeInTheDocument();
    expect(screen.getByText("⌘K")).toBeInTheDocument();
  });

  it("renders notification bell", () => {
    renderTopBar();
    expect(screen.getByRole("button", { name: /通知/i })).toBeInTheDocument();
  });

  it("renders theme toggle", () => {
    renderTopBar();
    expect(screen.getByRole("button", { name: /主题/i })).toBeInTheDocument();
  });

  it("renders user menu trigger", () => {
    renderTopBar();
    expect(screen.getByRole("button", { name: /用户菜单/i })).toBeInTheDocument();
  });

  it("last breadcrumb is not a link", () => {
    renderTopBar([
      { label: "首页", href: "/" },
      { label: "客户" },
    ]);
    const customerEl = screen.getByText("客户");
    expect(customerEl.closest("a")).toBeNull();
  });
});
