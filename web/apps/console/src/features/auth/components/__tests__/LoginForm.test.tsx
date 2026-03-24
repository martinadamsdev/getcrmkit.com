import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { LoginForm } from "../LoginForm";

describe("LoginForm", () => {
  const mockOnSubmit = vi.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it("should render email, password inputs and submit button", () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);
    expect(screen.getByLabelText(/邮箱/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/密码/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /登录/i })).toBeInTheDocument();
  });

  it("should render remember me checkbox", () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);
    expect(screen.getByLabelText(/记住我/i)).toBeInTheDocument();
  });

  it("should call onSubmit with form data", async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={mockOnSubmit} />);

    await user.type(screen.getByLabelText(/邮箱/i), "test@example.com");
    await user.type(screen.getByLabelText(/密码/i), "password123");
    await user.click(screen.getByRole("button", { name: /登录/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        email: "test@example.com",
        password: "password123",
        remember_me: false,
      });
    });
  });

  it("should submit with remember_me=true when checked", async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={mockOnSubmit} />);

    await user.type(screen.getByLabelText(/邮箱/i), "test@example.com");
    await user.type(screen.getByLabelText(/密码/i), "password123");
    await user.click(screen.getByLabelText(/记住我/i));
    await user.click(screen.getByRole("button", { name: /登录/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        email: "test@example.com",
        password: "password123",
        remember_me: true,
      });
    });
  });

  it("should display error message when provided", () => {
    render(<LoginForm onSubmit={mockOnSubmit} error="邮箱或密码错误" />);
    expect(screen.getByText("邮箱或密码错误")).toBeInTheDocument();
  });

  it("should disable submit button when loading", () => {
    render(<LoginForm onSubmit={mockOnSubmit} isLoading={true} />);
    expect(screen.getByRole("button", { name: /登录/i })).toBeDisabled();
  });
});
