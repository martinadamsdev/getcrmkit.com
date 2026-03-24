import { createFileRoute } from "@tanstack/react-router"

import { ScriptTemplateManager } from "../features/settings/components/ScriptTemplateManager"

export const Route = createFileRoute("/_app/settings/templates")({
  component: ScriptTemplateManager,
})
