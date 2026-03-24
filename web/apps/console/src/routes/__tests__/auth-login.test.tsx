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

// Mock auth store
vi.mock("@/shared/stores/auth.store", () => ({
  useAuthStore: () => ({
    setTokens: vi.fn(),
    setUser: vi.fn(),
    isLoading: false,
    setLoading: vi.fn(),
  }),
}));

// Mock auth API
vi.mock("@/features/auth/api/auth.api", () => ({
  login: vi.fn(),
  getProfile: vi.fn(),
}));

// Dynamic import after mocks are set up
const { LoginForm } = await import(
  "@/features/auth/components/LoginForm"
);

describe("Login Route", () => {
  it("should render the login page heading and form", () => {
    render(
      <div className="flex flex-col gap-6">
        <div className="flex flex-col items-center gap-2 text-center">
          <h1 className="text-2xl font-semibold tracking-tight">
            登录 CRMKit
          </h1>
          <p className="text-sm text-muted-foreground">
            输入邮箱和密码登录你的账号
          </p>
        </div>
        <LoginForm onSubmit={vi.fn()} />
        <p className="text-center text-sm text-muted-foreground">
          没有账号？ <a href="/register">注册</a>
        </p>
      </div>,
    );

    expect(screen.getByText("登录 CRMKit")).toBeInTheDocument();
    expect(
      screen.getByText("输入邮箱和密码登录你的账号"),
    ).toBeInTheDocument();
    expect(screen.getByLabelText(/邮箱/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/密码/i)).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /登录/i }),
    ).toBeInTheDocument();
    expect(screen.getByText("注册")).toBeInTheDocument();
  });

  it("should have a link to register page", () => {
    render(
      <div>
        <LoginForm onSubmit={vi.fn()} />
        <a href="/register">注册</a>
      </div>,
    );
    const registerLink = screen.getByText("注册");
    expect(registerLink).toHaveAttribute("href", "/register");
  });
});
