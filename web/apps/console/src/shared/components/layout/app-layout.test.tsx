import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { AppLayout } from "./app-layout";
import { SidebarProvider } from "@workspace/ui/components/sidebar";
import { TooltipProvider } from "@workspace/ui/components/tooltip";

// Mock router
vi.mock("@tanstack/react-router", async () => {
  const actual = await vi.importActual("@tanstack/react-router");
  return {
    ...actual,
    Outlet: () => <div data-testid="outlet">Outlet Content</div>,
    useRouterState: () => ({ location: { pathname: "/" } }),
    Link: ({ to, children, ...props }: any) => (
      <a href={to} {...props}>{children}</a>
    ),
  };
});

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

vi.mock("@/shared/hooks/use-nav-badges", () => ({
  useNavBadges: () => ({
    customers: 0,
    quotations: 0,
    orders: 0,
    follow_ups: 0,
  }),
}));

// Mock NotificationDropdown to avoid react-query dependency
vi.mock("./NotificationDropdown", () => ({
  NotificationDropdown: () => (
    <button type="button" aria-label="通知">Bell</button>
  ),
}));

describe("AppLayout", () => {
  it("renders sidebar", () => {
    render(
      <TooltipProvider>
        <SidebarProvider>
          <AppLayout />
        </SidebarProvider>
      </TooltipProvider>,
    );
    expect(screen.getByText("CRMKit")).toBeInTheDocument();
  });

  it("renders topbar", () => {
    render(
      <TooltipProvider>
        <SidebarProvider>
          <AppLayout />
        </SidebarProvider>
      </TooltipProvider>,
    );
    expect(screen.getByText("搜索...")).toBeInTheDocument();
  });

  it("renders outlet for child routes", () => {
    render(
      <TooltipProvider>
        <SidebarProvider>
          <AppLayout />
        </SidebarProvider>
      </TooltipProvider>,
    );
    expect(screen.getByTestId("outlet")).toBeInTheDocument();
  });
});
