import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { DeliveryAlertPanel } from "./DeliveryAlertPanel";
import type { DeliveryAlert } from "../types";

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

describe("DeliveryAlertPanel", () => {
  it("renders overdue and upcoming alerts", () => {
    const alerts: DeliveryAlert[] = [
      {
        order_id: "o1",
        order_number: "ORD-001",
        customer_name: "ABC Co",
        expected_date: "2026-03-20",
        status: "overdue",
      },
      {
        order_id: "o2",
        order_number: "ORD-002",
        customer_name: "DEF Co",
        expected_date: "2026-03-28",
        status: "within_7_days",
      },
    ];
    render(<DeliveryAlertPanel alerts={alerts} />);
    expect(screen.getByText("ORD-001")).toBeInTheDocument();
    expect(screen.getByText("逾期")).toBeInTheDocument();
    expect(screen.getByText("ORD-002")).toBeInTheDocument();
    expect(screen.getByText("7天内到期")).toBeInTheDocument();
  });

  it("renders empty state when no alerts", () => {
    render(<DeliveryAlertPanel alerts={[]} />);
    expect(screen.getByText("无发货预警")).toBeInTheDocument();
  });
});
