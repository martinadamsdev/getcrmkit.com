import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { FollowUpToolbar } from "../follow-up-toolbar";

describe("FollowUpToolbar", () => {
  const defaultProps = {
    onSearch: vi.fn(),
    onCreateClick: vi.fn(),
    onFilterToggle: vi.fn(),
    filtersOpen: false,
  };

  it("renders search input", () => {
    render(<FollowUpToolbar {...defaultProps} />);
    expect(
      screen.getByPlaceholderText("搜索跟进记录..."),
    ).toBeInTheDocument();
  });

  it("renders create button", () => {
    render(<FollowUpToolbar {...defaultProps} />);
    expect(
      screen.getByRole("button", { name: /新建跟进/ }),
    ).toBeInTheDocument();
  });

  it("calls onCreateClick when button clicked", async () => {
    const user = userEvent.setup();
    render(<FollowUpToolbar {...defaultProps} />);
    await user.click(screen.getByRole("button", { name: /新建跟进/ }));
    expect(defaultProps.onCreateClick).toHaveBeenCalledOnce();
  });

  it("renders filter toggle button", () => {
    render(<FollowUpToolbar {...defaultProps} />);
    expect(
      screen.getByRole("button", { name: /筛选/ }),
    ).toBeInTheDocument();
  });
});
