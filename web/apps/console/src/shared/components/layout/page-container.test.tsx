// web/apps/console/src/shared/components/layout/page-container.test.tsx
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { PageContainer } from "./page-container";

describe("PageContainer", () => {
  it("renders children", () => {
    render(
      <PageContainer>
        <div>Hello World</div>
      </PageContainer>,
    );
    expect(screen.getByText("Hello World")).toBeInTheDocument();
  });

  it("applies padding classes", () => {
    const { container } = render(
      <PageContainer>
        <div>Content</div>
      </PageContainer>,
    );
    const wrapper = container.firstElementChild;
    expect(wrapper?.className).toContain("p-6");
  });

  it("supports custom className", () => {
    const { container } = render(
      <PageContainer className="max-w-4xl">
        <div>Content</div>
      </PageContainer>,
    );
    const wrapper = container.firstElementChild;
    expect(wrapper?.className).toContain("max-w-4xl");
  });
});
