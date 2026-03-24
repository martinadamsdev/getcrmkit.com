import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { ScriptCard } from "../script-card";

describe("ScriptCard", () => {
  const template = {
    id: "abc-123",
    scene: "first_contact",
    title: "首次联系模板",
    content: "Dear customer, thank you for your inquiry...",
    language: "zh-CN",
    position: 0,
    is_system: true,
    created_at: "2026-01-01T00:00:00Z",
    updated_at: "2026-01-01T00:00:00Z",
  };

  it("renders title and content preview", () => {
    render(<ScriptCard template={template} />);
    expect(screen.getByText("首次联系模板")).toBeInTheDocument();
    expect(
      screen.getByText(/Dear customer, thank you/),
    ).toBeInTheDocument();
  });

  it("shows copy button", () => {
    render(<ScriptCard template={template} />);
    expect(
      screen.getByRole("button", { name: /复制/i }),
    ).toBeInTheDocument();
  });

  it("calls navigator.clipboard.writeText on copy click", async () => {
    const user = userEvent.setup();
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, "clipboard", {
      value: { writeText },
      writable: true,
      configurable: true,
    });
    render(<ScriptCard template={template} />);
    await user.click(screen.getByRole("button", { name: /复制/i }));
    expect(writeText).toHaveBeenCalledWith(template.content);
  });

  it("shows system badge for system templates", () => {
    render(<ScriptCard template={template} />);
    expect(screen.getByText("系统")).toBeInTheDocument();
  });

  it("does not show system badge for custom templates", () => {
    render(<ScriptCard template={{ ...template, is_system: false }} />);
    expect(screen.queryByText("系统")).not.toBeInTheDocument();
  });
});
