import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@workspace/ui/components/tabs"
import { Badge } from "@workspace/ui/components/badge"
import { CustomerInfoCard } from "./customer-info-card"
import { ContactList } from "./contact-list"
import { CustomerTimeline } from "./customer-timeline"
import { CustomerQuotations } from "./customer-quotations"
import { EmptyState } from "@/shared/components/data/empty-state"
import { Package } from "lucide-react"
import type { Customer360Response } from "../types"

type Customer360TabsProps = {
  data: Customer360Response
  onContactCreated?: () => void
  className?: string
}

export function Customer360Tabs({
  data,
  onContactCreated,
  className,
}: Customer360TabsProps) {
  const { customer, stats, recent_follow_ups, quotations } = data

  return (
    <Tabs defaultValue="info" className={className}>
      <TabsList>
        <TabsTrigger value="info">基本信息</TabsTrigger>
        <TabsTrigger value="contacts" className="gap-1.5">
          联系人
          {stats.contact_count > 0 && (
            <Badge variant="secondary" className="ml-1">
              {stats.contact_count}
            </Badge>
          )}
        </TabsTrigger>
        <TabsTrigger value="follow-ups" className="gap-1.5">
          跟进记录
          {stats.follow_up_count > 0 && (
            <Badge variant="secondary" className="ml-1">
              {stats.follow_up_count}
            </Badge>
          )}
        </TabsTrigger>
        <TabsTrigger value="quotations" className="gap-1.5">
          报价
          {stats.quotation_count > 0 && (
            <Badge variant="secondary" className="ml-1">
              {stats.quotation_count}
            </Badge>
          )}
        </TabsTrigger>
        <TabsTrigger value="orders" className="gap-1.5">
          订单
          {stats.order_count > 0 && (
            <Badge variant="secondary" className="ml-1">
              {stats.order_count}
            </Badge>
          )}
        </TabsTrigger>
      </TabsList>

      <TabsContent value="info" className="mt-4">
        <CustomerInfoCard customer={customer} />
      </TabsContent>

      <TabsContent value="contacts" className="mt-4">
        <ContactList
          customerId={customer.id}
          contacts={customer.contacts}
          onContactCreated={onContactCreated}
        />
      </TabsContent>

      <TabsContent value="follow-ups" className="mt-4">
        <CustomerTimeline
          customerId={customer.id}
          followUps={recent_follow_ups}
        />
      </TabsContent>

      <TabsContent value="quotations" className="mt-4">
        <CustomerQuotations quotations={quotations} />
      </TabsContent>

      <TabsContent value="orders" className="mt-4">
        <EmptyState
          icon={Package}
          title="暂无订单"
          description="客户还没有相关订单"
        />
      </TabsContent>
    </Tabs>
  )
}
