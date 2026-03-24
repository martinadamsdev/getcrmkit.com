import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { ServerErrorPage } from "./ServerErrorPage";

describe("ServerErrorPage", () => {
  it("renders error title and description", () => {
    render(<ServerErrorPage />);
    expect(screen.getByText("系统异常")).toBeInTheDocument();
    expect(screen.getByText(/服务器出了点问题/)).toBeInTheDocument();
  });

  it("has retry button that reloads", async () => {
    const reloadMock = vi.fn();
    Object.defineProperty(window, "location", {
      value: { reload: reloadMock },
      writable: true,
    });
    const user = userEvent.setup();
    render(<ServerErrorPage />);
    await user.click(screen.getByRole("button", { name: "重试" }));
    expect(reloadMock).toHaveBeenCalled();
  });
});
