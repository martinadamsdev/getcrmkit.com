import { render } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { DashboardSkeleton } from "./DashboardSkeleton";

describe("DashboardSkeleton", () => {
  it("renders 7 skeleton placeholders", () => {
    const { container } = render(<DashboardSkeleton />);
    // 5 stat skeletons + at least 2 content area skeletons
    const skeletons = container.querySelectorAll('[data-testid^="skeleton-"]');
    expect(skeletons.length).toBeGreaterThanOrEqual(7);
  });
});
