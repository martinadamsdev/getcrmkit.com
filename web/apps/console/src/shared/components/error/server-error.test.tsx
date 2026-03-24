import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ServerError } from "./server-error";

describe("ServerError", () => {
  it("renders 500 heading", () => {
    render(<ServerError />);
    expect(screen.getByText("500")).toBeInTheDocument();
  });

  it("renders error message", () => {
    render(<ServerError />);
    expect(screen.getByText("系统异常")).toBeInTheDocument();
  });

  it("renders retry button", () => {
    render(<ServerError />);
    expect(screen.getByRole("button", { name: /重试/i })).toBeInTheDocument();
  });

  it("calls onRetry when retry button is clicked", async () => {
    const user = userEvent.setup();
    const onRetry = vi.fn();
    render(<ServerError onRetry={onRetry} />);

    await user.click(screen.getByRole("button", { name: /重试/i }));
    expect(onRetry).toHaveBeenCalledOnce();
  });
});
