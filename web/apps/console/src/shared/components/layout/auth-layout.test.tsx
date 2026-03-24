import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { AuthLayout } from "./auth-layout";

vi.mock("@tanstack/react-router", async () => {
  const actual = await vi.importActual("@tanstack/react-router");
  return {
    ...actual,
    Outlet: () => <div data-testid="outlet">Auth Form</div>,
  };
});

describe("AuthLayout", () => {
  it("renders CRMKit brand", () => {
    render(<AuthLayout />);
    expect(screen.getByText("CRMKit")).toBeInTheDocument();
  });

  it("renders outlet for auth forms", () => {
    render(<AuthLayout />);
    expect(screen.getByTestId("outlet")).toBeInTheDocument();
  });

  it("is centered on screen", () => {
    const { container } = render(<AuthLayout />);
    const wrapper = container.firstElementChild;
    expect(wrapper?.className).toContain("min-h-svh");
    expect(wrapper?.className).toContain("items-center");
    expect(wrapper?.className).toContain("justify-center");
  });

  it("card has max-width constraint", () => {
    const { container } = render(<AuthLayout />);
    const card = container.querySelector("[data-testid='auth-card']");
    expect(card?.className).toContain("max-w-md");
  });
});
