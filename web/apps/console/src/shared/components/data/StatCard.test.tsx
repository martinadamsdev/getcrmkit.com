import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { StatCard } from "./StatCard";

describe("StatCard", () => {
  it("renders title and value", () => {
    render(<StatCard title="客户总数" value={150} />);
    expect(screen.getByText("客户总数")).toBeInTheDocument();
    expect(screen.getByText("150")).toBeInTheDocument();
  });

  it("renders with subtitle", () => {
    render(<StatCard title="报价单" value={45} subtitle="转化率 33.3%" />);
    expect(screen.getByText("转化率 33.3%")).toBeInTheDocument();
  });

  it("renders zero value (not hidden)", () => {
    render(<StatCard title="订单" value={0} />);
    expect(screen.getByText("0")).toBeInTheDocument();
  });

  it("is clickable when onClick provided", async () => {
    const onClick = vi.fn();
    const user = userEvent.setup();
    render(<StatCard title="客户" value={10} onClick={onClick} />);
    await user.click(screen.getByText("客户"));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it("renders icon when provided", () => {
    const Icon = () => <svg data-testid="icon" />;
    render(<StatCard title="测试" value={1} icon={<Icon />} />);
    expect(screen.getByTestId("icon")).toBeInTheDocument();
  });
});
