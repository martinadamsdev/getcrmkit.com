import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@workspace/ui/components/tabs"
import { Button } from "@workspace/ui/components/button"
import { Plus } from "lucide-react"

import { apiFetch } from "@/shared/api/fetcher"
import { CustomFieldCreateDialog } from "./CustomFieldCreateDialog"
import { CustomFieldTable } from "./CustomFieldTable"

const ENTITIES = [
  { value: "customer", label: "客户" },
  { value: "product", label: "产品" },
  { value: "contact", label: "联系人" },
]

export function CustomFieldManager() {
  const [entity, setEntity] = useState("customer")
  const [createOpen, setCreateOpen] = useState(false)

  const { data } = useQuery({
    queryKey: ["custom-field-definitions", entity],
    queryFn: async () => {
      const res = await apiFetch(`/api/v1/custom-field-definitions?entity=${entity}`)
      if (!res.ok) throw new Error("Failed to fetch custom fields")
      return res.json()
    },
  })

  return (
    <div className="max-w-3xl space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">自定义字段</h2>
        <Button onClick={() => setCreateOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          新建字段
        </Button>
      </div>

      <Tabs value={entity} onValueChange={setEntity}>
        <TabsList>
          {ENTITIES.map((e) => (
            <TabsTrigger key={e.value} value={e.value}>
              {e.label}
            </TabsTrigger>
          ))}
        </TabsList>
        {ENTITIES.map((e) => (
          <TabsContent key={e.value} value={e.value}>
            <CustomFieldTable
              fields={data?.items ?? []}
              entity={e.value}
            />
          </TabsContent>
        ))}
      </Tabs>

      <CustomFieldCreateDialog
        open={createOpen}
        onOpenChange={setCreateOpen}
        entity={entity}
      />
    </div>
  )
}
