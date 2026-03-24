import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { RegisterForm } from "../RegisterForm";

describe("RegisterForm", () => {
  const mockOnSubmit = vi.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it("should render all fields and submit button", () => {
    render(<RegisterForm onSubmit={mockOnSubmit} />);
    expect(screen.getByLabelText(/邮箱/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^密码$/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/确认密码/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/姓名/i)).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /注册/i }),
    ).toBeInTheDocument();
  });

  it("should call onSubmit with form data", async () => {
    const user = userEvent.setup();
    render(<RegisterForm onSubmit={mockOnSubmit} />);

    await user.type(screen.getByLabelText(/邮箱/i), "new@example.com");
    await user.type(screen.getByLabelText(/姓名/i), "New User");
    await user.type(screen.getByLabelText(/^密码$/i), "password123");
    await user.type(screen.getByLabelText(/确认密码/i), "password123");
    await user.click(screen.getByRole("button", { name: /注册/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        email: "new@example.com",
        password: "password123",
        name: "New User",
      });
    });
  });

  it("should show error when passwords do not match", async () => {
    const user = userEvent.setup();
    render(<RegisterForm onSubmit={mockOnSubmit} />);

    await user.type(screen.getByLabelText(/邮箱/i), "new@example.com");
    await user.type(screen.getByLabelText(/姓名/i), "New User");
    await user.type(screen.getByLabelText(/^密码$/i), "password123");
    await user.type(
      screen.getByLabelText(/确认密码/i),
      "differentpassword",
    );
    await user.click(screen.getByRole("button", { name: /注册/i }));

    expect(screen.getByText(/密码不一致/i)).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it("should display password strength indicator", async () => {
    const user = userEvent.setup();
    render(<RegisterForm onSubmit={mockOnSubmit} />);

    await user.type(screen.getByLabelText(/^密码$/i), "ab");
    expect(screen.getByText(/弱/i)).toBeInTheDocument();

    await user.clear(screen.getByLabelText(/^密码$/i));
    await user.type(screen.getByLabelText(/^密码$/i), "password1");
    expect(screen.getByText(/中/i)).toBeInTheDocument();

    await user.clear(screen.getByLabelText(/^密码$/i));
    await user.type(screen.getByLabelText(/^密码$/i), "P@ssw0rd123!");
    expect(screen.getByText(/强/i)).toBeInTheDocument();
  });

  it("should display error message when provided", () => {
    render(<RegisterForm onSubmit={mockOnSubmit} error="该邮箱已注册" />);
    expect(screen.getByText("该邮箱已注册")).toBeInTheDocument();
  });

  it("should disable submit button when loading", () => {
    render(<RegisterForm onSubmit={mockOnSubmit} isLoading={true} />);
    expect(
      screen.getByRole("button", { name: /注册/i }),
    ).toBeDisabled();
  });
});
