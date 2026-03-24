import { createFileRoute } from "@tanstack/react-router"

import { CompanyForm } from "../features/settings/components/CompanyForm"

export const Route = createFileRoute("/_app/settings/company")({
  component: CompanyForm,
})
