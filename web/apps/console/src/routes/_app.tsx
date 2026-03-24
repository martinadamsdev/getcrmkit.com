import { createFileRoute, redirect } from "@tanstack/react-router"
import { SidebarProvider } from "@workspace/ui/components/sidebar"
import { useAuthStore } from "@/shared/stores/auth.store"
import { AppLayout } from "@/shared/components/layout/app-layout"

export const Route = createFileRoute("/_app")({
  beforeLoad: () => {
    const { isAuthenticated } = useAuthStore.getState()
    if (!isAuthenticated) {
      throw redirect({ to: "/login" })
    }
  },
  component: AuthenticatedLayout,
})

function AuthenticatedLayout() {
  return (
    <SidebarProvider>
      <AppLayout />
    </SidebarProvider>
  )
}
