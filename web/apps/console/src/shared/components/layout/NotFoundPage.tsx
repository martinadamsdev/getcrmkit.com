import { useNavigate } from "@tanstack/react-router";
import { Button } from "@workspace/ui/components/button";
import { FileQuestion } from "lucide-react";

export function NotFoundPage() {
  const navigate = useNavigate();

  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center gap-6">
      <FileQuestion className="h-24 w-24 text-muted-foreground" />
      <div className="text-center">
        <h1 className="text-2xl font-semibold">页面未找到</h1>
        <p className="mt-2 text-muted-foreground">你访问的页面不存在</p>
      </div>
      <Button onClick={() => navigate({ to: "/" })}>返回首页</Button>
    </div>
  );
}
