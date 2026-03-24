import { AlertTriangle } from "lucide-react";
import { Button } from "@workspace/ui/components/button";

interface ServerErrorProps {
  onRetry?: () => void;
}

export function ServerError({ onRetry }: ServerErrorProps) {
  function handleRetry() {
    if (onRetry) {
      onRetry();
    } else {
      window.location.reload();
    }
  }

  return (
    <div className="flex min-h-svh flex-col items-center justify-center gap-4 text-center">
      <AlertTriangle className="size-16 text-destructive" />
      <h1 className="text-6xl font-bold">500</h1>
      <p className="text-lg text-muted-foreground">系统异常</p>
      <p className="max-w-sm text-sm text-muted-foreground">
        服务器遇到了一个错误，请稍后重试。
      </p>
      <Button onClick={handleRetry}>重试</Button>
    </div>
  );
}
