import { createFileRoute } from "@tanstack/react-router"

import { CustomFieldManager } from "../features/settings/components/CustomFieldManager"

export const Route = createFileRoute("/_app/settings/custom-fields")({
  component: CustomFieldManager,
})
