import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { RecentOrders } from "./RecentOrders";
import type { RecentOrder } from "../types";

vi.mock("@tanstack/react-router", () => ({
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

describe("RecentOrders", () => {
  it("renders order table", () => {
    const orders: RecentOrder[] = [
      {
        id: "o1",
        order_number: "ORD-001",
        customer_name: "ABC",
        amount: 10000,
        currency: "USD",
        status: "confirmed",
        created_at: "2026-03-22T10:00:00Z",
      },
    ];
    render(<RecentOrders orders={orders} />);
    expect(screen.getByText("ORD-001")).toBeInTheDocument();
    expect(screen.getByText("ABC")).toBeInTheDocument();
  });

  it("shows view-all link", () => {
    render(<RecentOrders orders={[]} />);
    expect(screen.getByText("全部")).toBeInTheDocument();
  });

  it("renders empty state", () => {
    render(<RecentOrders orders={[]} />);
    expect(screen.getByText("暂无订单")).toBeInTheDocument();
  });
});
