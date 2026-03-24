import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";
import type { ReactNode } from "react";
import { describe, expect, it, beforeAll, afterEach, afterAll } from "vitest";

import { useDashboard } from "./useDashboard";
import type { DashboardData } from "../types";

const MOCK_DASHBOARD: DashboardData = {
  stats: {
    total_customers: 150,
    total_quotations: 45,
    quotation_conversion_rate: 33.3,
    total_orders: 15,
    pending_follow_ups: 8,
    delivery_alerts: 3,
  },
  sales_summary: {
    yearly_sales_usd: 125000,
    monthly_sales_usd: 18500,
  },
  delivery_alerts: [],
  recent_quotations: [],
  overdue_follow_ups: [],
  order_distribution: [
    { status: "confirmed", count: 10 },
    { status: "shipped", count: 3 },
    { status: "delivered", count: 2 },
  ],
  recent_orders: [],
};

const server = setupServer(
  http.get("/api/v1/dashboard", () => HttpResponse.json(MOCK_DASHBOARD)),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("useDashboard", () => {
  function wrapper({ children }: { children: ReactNode }) {
    const queryClient = new QueryClient({
      defaultOptions: { queries: { retry: false } },
    });
    return (
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    );
  }

  it("fetches dashboard data", async () => {
    const { result } = renderHook(() => useDashboard(), { wrapper });
    await waitFor(() => {
      expect(result.current.data).toBeDefined();
      expect(result.current.data?.stats.total_customers).toBe(150);
    });
  });

  it("returns isLoading while fetching", () => {
    const { result } = renderHook(() => useDashboard(), { wrapper });
    expect(result.current.isLoading).toBe(true);
  });
});
