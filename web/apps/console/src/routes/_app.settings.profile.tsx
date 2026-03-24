import { createFileRoute } from "@tanstack/react-router"

import { ProfileForm } from "../features/settings/components/ProfileForm"

export const Route = createFileRoute("/_app/settings/profile")({
  component: ProfileForm,
})
