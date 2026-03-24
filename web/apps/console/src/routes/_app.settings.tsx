import { Outlet, createFileRoute } from "@tanstack/react-router"

import { SettingsSidebar } from "../features/settings/components/SettingsSidebar"

export const Route = createFileRoute("/_app/settings")({
  component: SettingsLayout,
})

function SettingsLayout() {
  return (
    <div className="flex gap-8 p-6">
      <SettingsSidebar />
      <div className="flex-1">
        <Outlet />
      </div>
    </div>
  )
}
