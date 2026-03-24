import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { RecentQuotations } from "./RecentQuotations";
import type { RecentQuotation } from "../types";

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

describe("RecentQuotations", () => {
  it("renders quotation table", () => {
    const quotations: RecentQuotation[] = [
      {
        id: "q1",
        customer_name: "ABC",
        product_name: "Widget",
        amount: 5000,
        currency: "USD",
        status: "sent",
        created_at: "2026-03-22T10:00:00Z",
      },
    ];
    render(<RecentQuotations quotations={quotations} />);
    expect(screen.getByText("ABC")).toBeInTheDocument();
    expect(screen.getByText("Widget")).toBeInTheDocument();
    expect(screen.getByText("$5,000")).toBeInTheDocument();
  });

  it("shows view-all link", () => {
    render(<RecentQuotations quotations={[]} />);
    expect(screen.getByText("全部")).toBeInTheDocument();
  });

  it("renders empty state", () => {
    render(<RecentQuotations quotations={[]} />);
    expect(screen.getByText("暂无报价")).toBeInTheDocument();
  });
});
