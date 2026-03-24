// web/apps/console/src/shared/components/layout/app-sidebar.tsx
import { Link, useRouterState } from "@tanstack/react-router";
import {
  LayoutDashboard,
  Users,
  MessageSquare,
  Package,
  FileText,
  ShoppingCart,
  Settings,
} from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuBadge,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@workspace/ui/components/sidebar";

const NAV_ITEMS = [
  { label: "看板", href: "/", icon: LayoutDashboard, badgeKey: null },
  { label: "客户", href: "/customers", icon: Users, badgeKey: "customers" },
  { label: "跟进", href: "/follow-ups", icon: MessageSquare, badgeKey: "follow_ups" },
  { label: "产品", href: "/products", icon: Package, badgeKey: null },
  { label: "报价", href: "/quotations", icon: FileText, badgeKey: "quotations" },
  { label: "订单", href: "/orders", icon: ShoppingCart, badgeKey: "orders" },
  { label: "设置", href: "/settings", icon: Settings, badgeKey: null },
] as const;

interface AppSidebarProps {
  badges?: Record<string, number>;
}

export function AppSidebar({ badges = {} }: AppSidebarProps) {
  const router = useRouterState();
  const currentPath = router.location.pathname;

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="border-b border-sidebar-border px-4 py-3">
        <div className="flex items-center gap-2">
          <div className="flex size-7 items-center justify-center rounded-lg bg-primary text-primary-foreground text-xs font-bold">
            C
          </div>
          <span className="text-sm font-semibold group-data-[collapsible=icon]:hidden">
            CRMKit
          </span>
        </div>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              {NAV_ITEMS.map((item) => {
                const isActive =
                  item.href === "/"
                    ? currentPath === "/"
                    : currentPath.startsWith(item.href);
                const badgeCount = item.badgeKey ? badges[item.badgeKey] ?? 0 : 0;

                return (
                  <SidebarMenuItem key={item.href}>
                    <SidebarMenuButton asChild isActive={isActive} tooltip={item.label}>
                      <Link to={item.href as string}>
                        <item.icon />
                        <span>{item.label}</span>
                      </Link>
                    </SidebarMenuButton>
                    {badgeCount > 0 ? (
                      <SidebarMenuBadge>{badgeCount}</SidebarMenuBadge>
                    ) : null}
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
