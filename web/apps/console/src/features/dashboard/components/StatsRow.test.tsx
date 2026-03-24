import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { StatsRow } from "./StatsRow";
import type { DashboardStats } from "../types";

vi.mock("@tanstack/react-router", () => ({
  useNavigate: () => vi.fn(),
}));

const STATS: DashboardStats = {
  total_customers: 150,
  total_quotations: 45,
  quotation_conversion_rate: 33.3,
  total_orders: 15,
  pending_follow_ups: 8,
  delivery_alerts: 3,
};

describe("StatsRow", () => {
  it("renders 5 stat cards", () => {
    render(<StatsRow stats={STATS} />);
    expect(screen.getByText("客户总数")).toBeInTheDocument();
    expect(screen.getByText("150")).toBeInTheDocument();
    expect(screen.getByText("报价单")).toBeInTheDocument();
    expect(screen.getByText("45")).toBeInTheDocument();
    expect(screen.getByText("成交订单")).toBeInTheDocument();
    expect(screen.getByText("15")).toBeInTheDocument();
    expect(screen.getByText("待跟进")).toBeInTheDocument();
    expect(screen.getByText("8")).toBeInTheDocument();
    expect(screen.getByText("发货预警")).toBeInTheDocument();
    expect(screen.getByText("3")).toBeInTheDocument();
  });

  it("shows conversion rate subtitle", () => {
    render(<StatsRow stats={STATS} />);
    expect(screen.getByText("转化率 33.3%")).toBeInTheDocument();
  });

  it("shows overdue badge on follow-ups", () => {
    render(<StatsRow stats={STATS} />);
    expect(screen.getByText("超15天")).toBeInTheDocument();
  });
});
