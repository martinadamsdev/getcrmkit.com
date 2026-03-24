import { createFileRoute, useNavigate, Link } from "@tanstack/react-router";
import {
  RegisterForm,
  type RegisterFormData,
} from "@/features/auth/components/RegisterForm";
import { register as registerApi } from "@/features/auth/api/auth.api";
import { useState } from "react";

export const Route = createFileRoute("/_auth/register")({
  component: RegisterPage,
});

function RegisterPage() {
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleRegister = async (data: RegisterFormData) => {
    setIsLoading(true);
    setError(null);
    try {
      await registerApi(data);
      navigate({ to: "/login" });
    } catch (err: unknown) {
      if (err instanceof Error && "status" in err) {
        const status = (err as { status: number }).status;
        if (status === 409) {
          setError("该邮箱已注册");
        } else if (status === 422) {
          setError("密码强度不足：需要至少 8 位，包含字母和数字");
        } else {
          setError(err.message ?? "注册失败，请稍后重试");
        }
      } else {
        setError("注册失败，请稍后重试");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col items-center gap-2 text-center">
        <h1 className="text-2xl font-semibold tracking-tight">
          注册 CRMKit
        </h1>
        <p className="text-sm text-muted-foreground">创建账号开始使用</p>
      </div>

      <RegisterForm
        onSubmit={handleRegister}
        error={error}
        isLoading={isLoading}
      />

      <p className="text-center text-sm text-muted-foreground">
        已有账号？{" "}
        <Link
          to="/login"
          className="text-accent underline-offset-4 hover:underline"
        >
          登录
        </Link>
      </p>
    </div>
  );
}
