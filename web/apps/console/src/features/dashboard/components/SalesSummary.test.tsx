import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { SalesSummary } from "./SalesSummary";

describe("SalesSummary", () => {
  it("renders yearly and monthly sales", () => {
    render(<SalesSummary yearlySalesUsd={125000} monthlySalesUsd={18500} />);
    expect(screen.getByText("年度销售额")).toBeInTheDocument();
    expect(screen.getByText("$125,000")).toBeInTheDocument();
    expect(screen.getByText("本月销售额")).toBeInTheDocument();
    expect(screen.getByText("$18,500")).toBeInTheDocument();
  });

  it("renders zero sales correctly", () => {
    render(<SalesSummary yearlySalesUsd={0} monthlySalesUsd={0} />);
    const zeros = screen.getAllByText("$0");
    expect(zeros).toHaveLength(2);
  });
});
