import { useState, type FormEvent } from "react";
import { Button } from "@workspace/ui/components/button";
import { Input } from "@workspace/ui/components/input";
import { Label } from "@workspace/ui/components/label";

export interface RegisterFormData {
  email: string;
  password: string;
  name: string;
}

interface RegisterFormProps {
  onSubmit: (data: RegisterFormData) => void | Promise<void>;
  error?: string | null;
  isLoading?: boolean;
}

function getPasswordStrength(
  password: string,
): { label: string; level: number } {
  if (password.length === 0) return { label: "", level: 0 };
  let score = 0;
  if (password.length >= 8) score++;
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;
  if (/\d/.test(password)) score++;
  if (/[^a-zA-Z0-9]/.test(password)) score++;

  if (score <= 1) return { label: "弱", level: 1 };
  if (score <= 2) return { label: "中", level: 2 };
  return { label: "强", level: 3 };
}

export function RegisterForm({
  onSubmit,
  error,
  isLoading = false,
}: RegisterFormProps) {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordError, setPasswordError] = useState<string | null>(null);

  const strength = getPasswordStrength(password);

  const strengthColors = ["", "bg-destructive", "bg-warning", "bg-success"];
  const strengthWidths = ["", "w-1/3", "w-2/3", "w-full"];

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setPasswordError("密码不一致");
      return;
    }
    setPasswordError(null);
    onSubmit({ email, password, name });
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      {error && (
        <div className="rounded-md bg-destructive/10 px-4 py-3 text-sm text-destructive">
          {error}
        </div>
      )}

      <div className="flex flex-col gap-2">
        <Label htmlFor="name">姓名</Label>
        <Input
          id="name"
          type="text"
          placeholder="你的姓名"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          autoComplete="name"
        />
      </div>

      <div className="flex flex-col gap-2">
        <Label htmlFor="email">邮箱</Label>
        <Input
          id="email"
          type="email"
          placeholder="you@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          autoComplete="email"
        />
      </div>

      <div className="flex flex-col gap-2">
        <Label htmlFor="password">密码</Label>
        <Input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          autoComplete="new-password"
        />
        {strength.level > 0 && (
          <div className="flex items-center gap-2">
            <div className="h-1.5 flex-1 rounded-full bg-muted">
              <div
                className={`h-full rounded-full transition-all ${strengthColors[strength.level]} ${strengthWidths[strength.level]}`}
              />
            </div>
            <span className="text-xs text-muted-foreground">
              {strength.label}
            </span>
          </div>
        )}
      </div>

      <div className="flex flex-col gap-2">
        <Label htmlFor="confirmPassword">确认密码</Label>
        <Input
          id="confirmPassword"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
          autoComplete="new-password"
        />
        {passwordError && (
          <p className="text-xs text-destructive">{passwordError}</p>
        )}
      </div>

      <Button type="submit" className="w-full" disabled={isLoading}>
        {isLoading ? "注册中..." : "注册"}
      </Button>
    </form>
  );
}
