import { Link, useMatchRoute } from "@tanstack/react-router"
import { User, Building2, MessageSquareText, Settings2 } from "lucide-react"
import { cn } from "@workspace/ui/lib/utils"

const NAV_ITEMS = [
  { to: "/settings/profile", label: "个人信息", icon: User },
  { to: "/settings/company", label: "公司信息", icon: Building2 },
  { to: "/settings/templates", label: "话术模板", icon: MessageSquareText },
  { to: "/settings/custom-fields", label: "自定义字段", icon: Settings2 },
] as const

export function SettingsSidebar() {
  const matchRoute = useMatchRoute()

  return (
    <nav className="flex w-56 flex-col gap-1 border-r border-border pr-6">
      {NAV_ITEMS.map(({ to, label, icon: Icon }) => {
        const isActive = matchRoute({ to })
        return (
          <Link
            key={to}
            to={to}
            className={cn(
              "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
              isActive
                ? "bg-secondary text-foreground"
                : "text-muted-foreground hover:bg-secondary/50 hover:text-foreground",
            )}
          >
            <Icon className="h-4 w-4" />
            {label}
          </Link>
        )
      })}
    </nav>
  )
}
