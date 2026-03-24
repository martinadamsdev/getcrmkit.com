import { Outlet } from "@tanstack/react-router";
import { Card, CardContent } from "@workspace/ui/components/card";

export function AuthLayout() {
  return (
    <div className="flex min-h-svh items-center justify-center bg-background p-4">
      <div className="w-full max-w-md space-y-6" data-testid="auth-card">
        {/* Brand */}
        <div className="flex flex-col items-center gap-2">
          <div className="flex size-10 items-center justify-center rounded-xl bg-primary text-primary-foreground font-bold">
            C
          </div>
          <span className="text-xl font-semibold">CRMKit</span>
        </div>

        {/* Auth form outlet */}
        <Card>
          <CardContent className="pt-6">
            <Outlet />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
