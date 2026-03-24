import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";

import { AppErrorBoundary } from "./AppErrorBoundary";

function ThrowingComponent() {
  throw new Error("Test error");
}

describe("AppErrorBoundary", () => {
  const originalConsoleError = console.error;
  beforeEach(() => {
    console.error = vi.fn();
  });
  afterEach(() => {
    console.error = originalConsoleError;
  });

  it("catches errors and shows fallback UI", () => {
    render(
      <AppErrorBoundary>
        <ThrowingComponent />
      </AppErrorBoundary>,
    );
    expect(screen.getByText("系统异常")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "重试" })).toBeInTheDocument();
  });

  it("renders children when no error", () => {
    render(
      <AppErrorBoundary>
        <p>正常内容</p>
      </AppErrorBoundary>,
    );
    expect(screen.getByText("正常内容")).toBeInTheDocument();
  });
});
