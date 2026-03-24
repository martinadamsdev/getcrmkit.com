import { render, screen, act } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { OfflineBanner } from "./OfflineBanner";

describe("OfflineBanner", () => {
  it("does not show when online", () => {
    const { container } = render(<OfflineBanner />);
    expect(container.textContent).toBe("");
  });

  it("shows banner when offline", () => {
    render(<OfflineBanner />);
    act(() => {
      window.dispatchEvent(new Event("offline"));
    });
    expect(screen.getByText("网络已断开，正在重连...")).toBeInTheDocument();
  });

  it("hides banner when back online", () => {
    render(<OfflineBanner />);
    act(() => {
      window.dispatchEvent(new Event("offline"));
    });
    expect(screen.getByText("网络已断开，正在重连...")).toBeInTheDocument();
    act(() => {
      window.dispatchEvent(new Event("online"));
    });
    expect(
      screen.queryByText("网络已断开，正在重连..."),
    ).not.toBeInTheDocument();
  });
});
