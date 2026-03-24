import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { ReportButtons } from "../report-buttons";

describe("ReportButtons", () => {
  const defaultProps = {
    period: "daily" as const,
    onPeriodChange: vi.fn(),
    onExport: vi.fn(),
  };

  it("renders all period options", () => {
    render(<ReportButtons {...defaultProps} />);
    expect(screen.getByText("日报")).toBeInTheDocument();
    expect(screen.getByText("周报")).toBeInTheDocument();
    expect(screen.getByText("月报")).toBeInTheDocument();
    expect(screen.getByText("年报")).toBeInTheDocument();
  });

  it("highlights active period", () => {
    render(<ReportButtons {...defaultProps} period="weekly" />);
    const weeklyBtn = screen.getByText("周报");
    expect(weeklyBtn.closest("[data-state]")).toHaveAttribute(
      "data-state",
      "on",
    );
  });

  it("calls onPeriodChange when toggled", async () => {
    const user = userEvent.setup();
    render(<ReportButtons {...defaultProps} />);
    await user.click(screen.getByText("月报"));
    expect(defaultProps.onPeriodChange).toHaveBeenCalledWith("monthly");
  });

  it("renders export button", () => {
    render(<ReportButtons {...defaultProps} />);
    expect(
      screen.getByRole("button", { name: /导出/ }),
    ).toBeInTheDocument();
  });

  it("calls onExport when export button clicked", async () => {
    const user = userEvent.setup();
    render(<ReportButtons {...defaultProps} />);
    await user.click(screen.getByRole("button", { name: /导出/ }));
    expect(defaultProps.onExport).toHaveBeenCalledOnce();
  });
});
