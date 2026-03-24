import { useEffect, useRef } from "react"
import { HeadContent, Outlet, Scripts, createRootRoute } from "@tanstack/react-router"
import { setupAuthInterceptor } from "@/shared/api/interceptors"
import { useThemeEffect } from "@/shared/hooks/use-theme-effect"
import { NotFound } from "@/shared/components/error/not-found"
import { I18nProvider } from "@/shared/i18n/context"

import appCss from "@workspace/ui/globals.css?url"

export const Route = createRootRoute({
  head: () => ({
    meta: [
      { charSet: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { title: "CRMKit Console" },
    ],
    links: [
      { rel: "stylesheet", href: appCss },
    ],
  }),
  shellComponent: RootDocument,
  notFoundComponent: NotFound,
  component: () => <Outlet />,
})

function RootDocument({ children }: { children: React.ReactNode }) {
  useThemeEffect()

  const interceptorSetup = useRef(false)
  useEffect(() => {
    if (!interceptorSetup.current) {
      setupAuthInterceptor()
      interceptorSetup.current = true
    }
  }, [])

  return (
    <html lang="zh-CN">
      <head>
        <HeadContent />
      </head>
      <body>
        <I18nProvider>
          {children}
        </I18nProvider>
        <Scripts />
      </body>
    </html>
  )
}
