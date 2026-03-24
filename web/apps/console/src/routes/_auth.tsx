import { createFileRoute, redirect } from "@tanstack/react-router"
import { useAuthStore } from "@/shared/stores/auth.store"
import { AuthLayout } from "@/shared/components/layout/auth-layout"

export const Route = createFileRoute("/_auth")({
  beforeLoad: () => {
    const { isAuthenticated } = useAuthStore.getState()
    if (isAuthenticated) {
      throw redirect({ to: "/" })
    }
  },
  component: AuthLayout,
})
