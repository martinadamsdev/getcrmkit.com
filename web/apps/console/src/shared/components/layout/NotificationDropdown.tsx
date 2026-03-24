import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Button } from "@workspace/ui/components/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@workspace/ui/components/dropdown-menu"
import { Badge } from "@workspace/ui/components/badge"
import { Bell } from "lucide-react"
import { formatDistanceToNow } from "date-fns"
import { zhCN, enUS } from "date-fns/locale"
import { useUIStore } from "@/shared/stores/ui.store"
import { apiFetch } from "@/shared/api/fetcher"

interface Notification {
  id: string
  title: string
  body: string
  read: boolean
  created_at: string
}

export function NotificationDropdown() {
  const queryClient = useQueryClient()
  const locale = useUIStore((s) => s.locale)
  const dateFnsLocale = locale === "en" ? enUS : zhCN

  const { data } = useQuery<{ items: Notification[]; total: number }>({
    queryKey: ["notifications"],
    queryFn: async () => {
      const res = await apiFetch("/api/v1/notifications?unread=true")
      if (!res.ok) throw new Error("Failed to fetch notifications")
      return res.json()
    },
    staleTime: 30_000,
    refetchInterval: 30_000,
  })

  const markRead = useMutation({
    mutationFn: async (id: string) => {
      await apiFetch(`/api/v1/notifications/${id}/read`, { method: "PATCH" })
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notifications"] })
    },
  })

  const markAllRead = useMutation({
    mutationFn: async () => {
      await apiFetch("/api/v1/notifications/read-all", { method: "POST" })
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notifications"] })
    },
  })

  const notifications = data?.items ?? []
  const unreadCount = notifications.filter((n) => !n.read).length

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon" className="relative" aria-label="通知">
          <Bell className="h-4 w-4" />
          {unreadCount > 0 && (
            <Badge
              variant="destructive"
              className="absolute -right-1 -top-1 h-5 min-w-5 px-1 text-xs"
            >
              {unreadCount}
            </Badge>
          )}
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-80">
        {notifications.length === 0 ? (
          <div className="py-6 text-center text-sm text-muted-foreground">
            暂无通知
          </div>
        ) : (
          <>
            {notifications.map((notification) => (
              <DropdownMenuItem
                key={notification.id}
                className="flex flex-col items-start gap-1 py-3"
                onClick={() => markRead.mutate(notification.id)}
              >
                <span className="text-sm font-medium">{notification.title}</span>
                <span className="text-xs text-muted-foreground">{notification.body}</span>
                <span className="text-xs text-muted-foreground">
                  {formatDistanceToNow(new Date(notification.created_at), {
                    addSuffix: true,
                    locale: dateFnsLocale,
                  })}
                </span>
              </DropdownMenuItem>
            ))}
            <DropdownMenuSeparator />
            <DropdownMenuItem
              className="justify-center text-sm"
              onClick={() => markAllRead.mutate()}
            >
              全部标为已读
            </DropdownMenuItem>
          </>
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
