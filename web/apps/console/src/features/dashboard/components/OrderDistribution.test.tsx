import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { OrderDistribution } from "./OrderDistribution";
import type { OrderDistributionItem } from "../types";

describe("OrderDistribution", () => {
  it("renders donut chart with data", () => {
    const data: OrderDistributionItem[] = [
      { status: "confirmed", count: 10 },
      { status: "shipped", count: 5 },
      { status: "delivered", count: 3 },
    ];
    render(<OrderDistribution data={data} />);
    expect(screen.getByText("订单分布")).toBeInTheDocument();
  });

  it("renders empty state when no data", () => {
    render(<OrderDistribution data={[]} />);
    expect(screen.getByText("暂无数据")).toBeInTheDocument();
  });
});
