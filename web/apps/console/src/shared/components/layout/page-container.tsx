// web/apps/console/src/shared/components/layout/page-container.tsx
import type { ReactNode } from "react";
import { cn } from "@workspace/ui/lib/utils";

interface PageContainerProps {
  children: ReactNode;
  className?: string;
}

export function PageContainer({ children, className }: PageContainerProps) {
  return (
    <div className={cn("flex-1 space-y-6 p-6", className)}>
      {children}
    </div>
  );
}
