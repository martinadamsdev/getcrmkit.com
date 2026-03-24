// web/apps/console/src/shared/components/layout/top-bar.tsx
import { Link } from "@tanstack/react-router";
import { Search, User } from "lucide-react";
import { Button } from "@workspace/ui/components/button";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@workspace/ui/components/breadcrumb";
import { SidebarTrigger } from "@workspace/ui/components/sidebar";
import { Separator } from "@workspace/ui/components/separator";
import { ThemeToggle } from "@/shared/components/theme-toggle";
import { NotificationDropdown } from "./NotificationDropdown";
import { LocaleSwitcher } from "./LocaleSwitcher";
import { Fragment } from "react";

interface BreadcrumbEntry {
  label: string;
  href?: string;
}

interface TopBarProps {
  breadcrumbs: BreadcrumbEntry[];
}

export function TopBar({ breadcrumbs }: TopBarProps) {
  return (
    <header className="flex h-14 shrink-0 items-center gap-2 border-b px-4">
      <SidebarTrigger className="-ml-1" />
      <Separator orientation="vertical" className="mr-2 h-4" />

      {/* Breadcrumbs */}
      <Breadcrumb className="flex-1">
        <BreadcrumbList>
          {breadcrumbs.map((item, index) => {
            const isLast = index === breadcrumbs.length - 1;
            return (
              <Fragment key={item.label}>
                {index > 0 ? <BreadcrumbSeparator /> : null}
                <BreadcrumbItem>
                  {isLast || !item.href ? (
                    <BreadcrumbPage>{item.label}</BreadcrumbPage>
                  ) : (
                    <BreadcrumbLink asChild>
                      <Link to={item.href}>{item.label}</Link>
                    </BreadcrumbLink>
                  )}
                </BreadcrumbItem>
              </Fragment>
            );
          })}
        </BreadcrumbList>
      </Breadcrumb>

      {/* Search trigger */}
      <Button
        variant="outline"
        className="hidden w-64 justify-start gap-2 text-muted-foreground md:flex"
        aria-label="搜索"
      >
        <Search className="size-4" />
        <span className="flex-1 text-left text-sm">搜索...</span>
        <kbd className="pointer-events-none rounded border bg-muted px-1.5 text-xs font-medium text-muted-foreground">
          ⌘K
        </kbd>
      </Button>

      {/* Notification bell */}
      <NotificationDropdown />

      {/* Locale switcher */}
      <LocaleSwitcher />

      {/* Theme toggle */}
      <ThemeToggle />

      {/* User menu */}
      <Button variant="ghost" size="icon" aria-label="用户菜单">
        <User className="size-4" />
      </Button>
    </header>
  );
}
