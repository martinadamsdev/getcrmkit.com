import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { NotFound } from "./not-found";

vi.mock("@tanstack/react-router", async () => {
  const actual = await vi.importActual("@tanstack/react-router");
  return {
    ...actual,
    Link: ({ to, children, ...props }: any) => (
      <a href={to} {...props}>{children}</a>
    ),
  };
});

describe("NotFound", () => {
  it("renders 404 heading", () => {
    render(<NotFound />);
    expect(screen.getByText("404")).toBeInTheDocument();
  });

  it("renders descriptive message", () => {
    render(<NotFound />);
    expect(screen.getByText("页面未找到")).toBeInTheDocument();
  });

  it("renders link back to home", () => {
    render(<NotFound />);
    const link = screen.getByRole("link", { name: /返回首页/i });
    expect(link).toHaveAttribute("href", "/");
  });
});
