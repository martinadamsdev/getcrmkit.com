import { Button } from "@workspace/ui/components/button";
import { ServerCrash } from "lucide-react";

export function ServerErrorPage() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center gap-6">
      <ServerCrash className="h-24 w-24 text-muted-foreground" />
      <div className="text-center">
        <h1 className="text-2xl font-semibold">系统异常</h1>
        <p className="mt-2 text-muted-foreground">
          服务器出了点问题，请稍后重试
        </p>
      </div>
      <Button onClick={() => window.location.reload()}>重试</Button>
    </div>
  );
}
