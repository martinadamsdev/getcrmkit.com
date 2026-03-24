import { render, screen, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";
import { describe, expect, it, vi, beforeAll, afterEach, afterAll } from "vitest";

import { DashboardPage } from "./DashboardPage";
import type { DashboardData } from "../types";

vi.mock("@tanstack/react-router", () => ({
  useNavigate: () => vi.fn(),
  Link: ({
    children,
    to,
    ...props
  }: { children: React.ReactNode; to: string; [key: string]: unknown }) => (
    <a href={to} {...props}>
      {children}
    </a>
  ),
}));

const MOCK_DASHBOARD: DashboardData = {
  stats: {
    total_customers: 150,
    total_quotations: 45,
    quotation_conversion_rate: 33.3,
    total_orders: 15,
    pending_follow_ups: 8,
    delivery_alerts: 3,
  },
  sales_summary: { yearly_sales_usd: 125000, monthly_sales_usd: 18500 },
  delivery_alerts: [],
  recent_quotations: [],
  overdue_follow_ups: [],
  order_distribution: [],
  recent_orders: [],
};

const server = setupServer(
  http.get("/api/v1/dashboard", () => HttpResponse.json(MOCK_DASHBOARD)),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

function renderWithProviders(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>,
  );
}

describe("DashboardPage", () => {
  it("shows skeleton while loading", () => {
    renderWithProviders(<DashboardPage />);
    expect(
      document.querySelector('[data-testid^="skeleton-"]'),
    ).toBeInTheDocument();
  });

  it("renders all dashboard sections after loading", async () => {
    renderWithProviders(<DashboardPage />);
    await waitFor(() => {
      expect(screen.getByText("客户总数")).toBeInTheDocument();
      expect(screen.getByText("150")).toBeInTheDocument();
      expect(screen.getByText("年度销售额")).toBeInTheDocument();
      expect(screen.getByText("$125,000")).toBeInTheDocument();
    });
  });

  it("renders empty states for new users", async () => {
    server.use(
      http.get("/api/v1/dashboard", () =>
        HttpResponse.json({
          ...MOCK_DASHBOARD,
          stats: {
            total_customers: 0,
            total_quotations: 0,
            quotation_conversion_rate: 0,
            total_orders: 0,
            pending_follow_ups: 0,
            delivery_alerts: 0,
          },
          sales_summary: { yearly_sales_usd: 0, monthly_sales_usd: 0 },
        }),
      ),
    );
    renderWithProviders(<DashboardPage />);
    await waitFor(() => {
      const zeros = screen.getAllByText("0");
      expect(zeros.length).toBeGreaterThan(0);
      expect(screen.getByText("暂无报价")).toBeInTheDocument();
      expect(screen.getByText("暂无订单")).toBeInTheDocument();
      expect(screen.getByText("所有客户都已跟进")).toBeInTheDocument();
      expect(screen.getByText("无发货预警")).toBeInTheDocument();
    });
  });
});
