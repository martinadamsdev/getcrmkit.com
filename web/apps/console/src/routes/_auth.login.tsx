import { createFileRoute, useNavigate, Link } from "@tanstack/react-router";
import {
  LoginForm,
  type LoginFormData,
} from "@/features/auth/components/LoginForm";
import {
  login as loginApi,
  getProfile,
} from "@/features/auth/api/auth.api";
import { useAuthStore } from "@/shared/stores/auth.store";
import { useState } from "react";

export const Route = createFileRoute("/_auth/login")({
  component: LoginPage,
});

function LoginPage() {
  const navigate = useNavigate();
  const { setTokens, setUser, isLoading, setLoading } = useAuthStore();
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (data: LoginFormData) => {
    setLoading(true);
    setError(null);
    try {
      const tokens = await loginApi(data);
      setTokens(tokens.access_token, tokens.refresh_token);

      const profile = await getProfile(tokens.access_token);
      setUser(profile);

      navigate({ to: "/" });
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("登录失败，请检查邮箱和密码");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col items-center gap-2 text-center">
        <h1 className="text-2xl font-semibold tracking-tight">
          登录 CRMKit
        </h1>
        <p className="text-sm text-muted-foreground">
          输入邮箱和密码登录你的账号
        </p>
      </div>

      <LoginForm
        onSubmit={handleLogin}
        error={error}
        isLoading={isLoading}
      />

      <p className="text-center text-sm text-muted-foreground">
        没有账号？{" "}
        <Link
          to="/register"
          className="text-accent underline-offset-4 hover:underline"
        >
          注册
        </Link>
      </p>
    </div>
  );
}
