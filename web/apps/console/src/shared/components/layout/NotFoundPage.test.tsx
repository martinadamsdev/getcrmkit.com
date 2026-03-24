import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { NotFoundPage } from "./NotFoundPage";

const mockNavigate = vi.fn();
vi.mock("@tanstack/react-router", () => ({
  useNavigate: () => mockNavigate,
}));

describe("NotFoundPage", () => {
  it("renders 404 title and description", () => {
    render(<NotFoundPage />);
    expect(screen.getByText("页面未找到")).toBeInTheDocument();
    expect(screen.getByText("你访问的页面不存在")).toBeInTheDocument();
  });

  it("has go-home button that navigates to /", async () => {
    const user = userEvent.setup();
    render(<NotFoundPage />);
    await user.click(screen.getByRole("button", { name: "返回首页" }));
    expect(mockNavigate).toHaveBeenCalledWith({ to: "/" });
  });
});
