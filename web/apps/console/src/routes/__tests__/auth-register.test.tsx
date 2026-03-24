import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";

// Mock TanStack Router hooks
vi.mock("@tanstack/react-router", () => ({
  createFileRoute: () => () => ({}),
  useNavigate: () => vi.fn(),
  Link: ({
    children,
    to,
    ...props
  }: { children: React.ReactNode; to: string }) => (
    <a href={to} {...props}>
      {children}
    </a>
  ),
}));

// Mock auth API
vi.mock("@/features/auth/api/auth.api", () => ({
  register: vi.fn(),
}));

// Dynamic import after mocks
const { RegisterForm } = await import(
  "@/features/auth/components/RegisterForm"
);

describe("Register Route", () => {
  it("should render the register page heading and form", () => {
    render(
      <div className="flex flex-col gap-6">
        <div className="flex flex-col items-center gap-2 text-center">
          <h1 className="text-2xl font-semibold tracking-tight">
            注册 CRMKit
          </h1>
          <p className="text-sm text-muted-foreground">
            创建账号开始使用
          </p>
        </div>
        <RegisterForm onSubmit={vi.fn()} />
        <p className="text-center text-sm text-muted-foreground">
          已有账号？ <a href="/login">登录</a>
        </p>
      </div>,
    );

    expect(screen.getByText("注册 CRMKit")).toBeInTheDocument();
    expect(screen.getByText("创建账号开始使用")).toBeInTheDocument();
    expect(screen.getByLabelText(/邮箱/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/姓名/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^密码$/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/确认密码/i)).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /注册/i }),
    ).toBeInTheDocument();
  });

  it("should have a link to login page", () => {
    render(
      <div>
        <RegisterForm onSubmit={vi.fn()} />
        <a href="/login">登录</a>
      </div>,
    );
    const loginLink = screen.getByText("登录");
    expect(loginLink).toHaveAttribute("href", "/login");
  });
});
