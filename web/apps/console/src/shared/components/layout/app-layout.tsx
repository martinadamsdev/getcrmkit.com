import { Outlet } from "@tanstack/react-router";
import { SidebarInset } from "@workspace/ui/components/sidebar";
import { AppSidebar } from "./app-sidebar";
import { TopBar } from "./top-bar";
import { AppErrorBoundary } from "./AppErrorBoundary";
import { OfflineBanner } from "./OfflineBanner";
import { useNavBadges } from "@/shared/hooks/use-nav-badges";

export function AppLayout() {
  const badges = useNavBadges();

  return (
    <>
      <OfflineBanner />
      <AppSidebar badges={badges} />
      <SidebarInset>
        <TopBar breadcrumbs={[{ label: "首页", href: "/" }]} />
        <main className="flex-1 overflow-auto">
          <AppErrorBoundary>
            <Outlet />
          </AppErrorBoundary>
        </main>
      </SidebarInset>
    </>
  );
}
