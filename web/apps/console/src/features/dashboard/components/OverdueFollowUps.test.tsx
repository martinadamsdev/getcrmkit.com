import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { OverdueFollowUps } from "./OverdueFollowUps";
import type { OverdueFollowUp } from "../types";

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

describe("OverdueFollowUps", () => {
  it("renders overdue customers with red badges", () => {
    const followUps: OverdueFollowUp[] = [
      {
        customer_id: "c1",
        customer_name: "ABC Trading",
        days_since_last_follow_up: 22,
      },
      {
        customer_id: "c2",
        customer_name: "XYZ Corp",
        days_since_last_follow_up: 18,
      },
    ];
    render(<OverdueFollowUps followUps={followUps} />);
    expect(screen.getByText("ABC Trading")).toBeInTheDocument();
    expect(screen.getByText("22天未跟进")).toBeInTheDocument();
    expect(screen.getByText("XYZ Corp")).toBeInTheDocument();
    expect(screen.getByText("18天未跟进")).toBeInTheDocument();
  });

  it("renders positive empty state", () => {
    render(<OverdueFollowUps followUps={[]} />);
    expect(screen.getByText("所有客户都已跟进")).toBeInTheDocument();
  });
});
