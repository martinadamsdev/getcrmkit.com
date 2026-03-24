import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@workspace/ui/components/tabs"
import { Card, CardContent } from "@workspace/ui/components/card"

interface OrderNotesSectionProps {
  internalNotes: string
  customerNotes: string
  onInternalNotesChange: (value: string) => void
  onCustomerNotesChange: (value: string) => void
  disabled: boolean
}

export function OrderNotesSection({
  internalNotes,
  customerNotes,
  onInternalNotesChange,
  onCustomerNotesChange,
  disabled,
}: OrderNotesSectionProps) {
  return (
    <Card>
      <CardContent className="pt-6">
        <Tabs defaultValue="internal">
          <TabsList>
            <TabsTrigger value="internal">内部备注</TabsTrigger>
            <TabsTrigger value="customer">客户备注</TabsTrigger>
          </TabsList>
          <TabsContent value="internal">
            <textarea
              className="mt-2 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              rows={4}
              value={internalNotes}
              onChange={(e) => onInternalNotesChange(e.target.value)}
              placeholder="内部备注（仅自己可见）..."
              disabled={disabled}
            />
            <p className="mt-1 text-xs text-muted-foreground">
              此备注仅供内部使用，不会显示给客户
            </p>
          </TabsContent>
          <TabsContent value="customer">
            <textarea
              className="mt-2 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              rows={4}
              value={customerNotes}
              onChange={(e) => onCustomerNotesChange(e.target.value)}
              placeholder="客户备注（可发送给客户）..."
              disabled={disabled}
            />
            <p className="mt-1 text-xs text-muted-foreground">
              此备注可在导出文件中显示给客户
            </p>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}
