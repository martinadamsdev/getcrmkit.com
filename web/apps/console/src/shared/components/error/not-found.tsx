import { Link } from "@tanstack/react-router";
import { FileQuestion } from "lucide-react";
import { Button } from "@workspace/ui/components/button";

export function NotFound() {
  return (
    <div className="flex min-h-svh flex-col items-center justify-center gap-4 text-center">
      <FileQuestion className="size-16 text-muted-foreground" />
      <h1 className="text-6xl font-bold">404</h1>
      <p className="text-lg text-muted-foreground">页面未找到</p>
      <p className="max-w-sm text-sm text-muted-foreground">
        你访问的页面不存在或已被移除。
      </p>
      <Button asChild>
        <Link to="/">返回首页</Link>
      </Button>
    </div>
  );
}
