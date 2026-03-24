import { useState } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import { Save, Loader2 } from "lucide-react"
import { Button } from "@workspace/ui/components/button"
import { Card, CardContent, CardHeader, CardTitle } from "@workspace/ui/components/card"
import { Label } from "@workspace/ui/components/label"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@workspace/ui/components/table"
import { MoneyDisplay } from "@/shared/components/data/money-display"
import { OrderStatusBadge } from "./OrderStatusBadge"
import { PaymentStatusBadge } from "./PaymentStatusBadge"
import { OrderNotesSection } from "./OrderNotesSection"
import { ShippingInfoCard } from "./ShippingInfoCard"
import { GeneratePIButton } from "./GeneratePIButton"
import { OrderStatusActions } from "./OrderStatusActions"
import type { OrderStatus } from "@/shared/lib/constants"
import { apiFetch } from "@/shared/api/fetcher"

interface OrderDetailProps {
  order: any
}

export function OrderDetail({ order }: OrderDetailProps) {
  const queryClient = useQueryClient()
  const status: OrderStatus = order.status
  const [internalNotes, setInternalNotes] = useState(
    order.internal_notes ?? "",
  )
  const [customerNotes, setCustomerNotes] = useState(
    order.customer_notes ?? "",
  )
  const [shipping, setShipping] = useState({
    carrier: order.carrier ?? "",
    domesticTrackingNo: order.domestic_tracking_no ?? "",
    internationalTrackingNo: order.international_tracking_no ?? "",
  })

  const transitionMutation = useMutation({
    mutationFn: async (targetStatus: OrderStatus) => {
      const res = await apiFetch(`/api/v1/orders/${order.id}/status`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: targetStatus }),
      })
      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error(err.detail ?? "Status transition failed")
      }
      return res.json()
    },
    onSuccess: () => {
      toast.success("订单状态已更新")
      queryClient.invalidateQueries({ queryKey: ["orders"] })
      queryClient.invalidateQueries({
        queryKey: ["order", order.id],
      })
    },
    onError: (err) => {
      toast.error(err instanceof Error ? err.message : "状态变更失败")
    },
  })

  const saveMutation = useMutation({
    mutationFn: async () => {
      const res = await apiFetch(`/api/v1/orders/${order.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          internal_notes: internalNotes,
          customer_notes: customerNotes,
          carrier: shipping.carrier,
          domestic_tracking_no: shipping.domesticTrackingNo,
          international_tracking_no: shipping.internationalTrackingNo,
        }),
      })
      if (!res.ok) throw new Error("Save failed")
      return res.json()
    },
    onSuccess: () => {
      toast.success("订单已保存")
      queryClient.invalidateQueries({ queryKey: ["order", order.id] })
    },
    onError: () => {
      toast.error("保存失败，请重试")
    },
  })

  const isTerminal = status === "completed" || status === "cancelled"

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <h2 className="text-2xl font-semibold">{order.order_no}</h2>
            <OrderStatusBadge status={status} />
            <PaymentStatusBadge status={order.payment_status} />
          </div>
          <p className="text-muted-foreground">
            {order.customer_name}
            {order.internal_no && (
              <span className="ml-2">内部编号: {order.internal_no}</span>
            )}
          </p>
        </div>
        <div className="flex gap-2">
          <GeneratePIButton orderId={order.id} />
          <Button
            onClick={() => saveMutation.mutate()}
            disabled={saveMutation.isPending || isTerminal}
          >
            {saveMutation.isPending ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <Save className="mr-2 h-4 w-4" />
            )}
            保存
          </Button>
        </div>
      </div>

      {/* Basic Info */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base">基本信息</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4 text-sm lg:grid-cols-4">
            <div>
              <Label className="text-muted-foreground">金额</Label>
              <p className="mt-1 font-medium">
                <MoneyDisplay
                  amount={order.total_amount}
                  currency={order.currency}
                />
              </p>
            </div>
            <div>
              <Label className="text-muted-foreground">贸易条款</Label>
              <p className="mt-1 font-medium">{order.trade_term ?? "—"}</p>
            </div>
            <div>
              <Label className="text-muted-foreground">付款条件</Label>
              <p className="mt-1 font-medium">
                {order.payment_term ?? "—"}
              </p>
            </div>
            <div>
              <Label className="text-muted-foreground">创建日期</Label>
              <p className="mt-1 font-medium">
                {new Date(order.created_at).toLocaleDateString("zh-CN")}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Line Items */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base">产品明细</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>产品</TableHead>
                <TableHead className="w-[100px]">数量</TableHead>
                <TableHead className="w-[120px]">单价</TableHead>
                <TableHead className="w-[120px]">小计</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {(order.items ?? []).map((item: any) => (
                <TableRow key={item.id}>
                  <TableCell className="font-medium">
                    {item.product_name}
                  </TableCell>
                  <TableCell>{item.quantity}</TableCell>
                  <TableCell>
                    <MoneyDisplay
                      amount={item.unit_price}
                      currency={item.currency ?? order.currency}
                    />
                  </TableCell>
                  <TableCell>
                    <MoneyDisplay
                      amount={item.subtotal}
                      currency={item.currency ?? order.currency}
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Two-column: Shipping + Notes */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <ShippingInfoCard
          carrier={shipping.carrier}
          domesticTrackingNo={shipping.domesticTrackingNo}
          internationalTrackingNo={shipping.internationalTrackingNo}
          onChange={setShipping}
          disabled={isTerminal}
        />
        <OrderNotesSection
          internalNotes={internalNotes}
          customerNotes={customerNotes}
          onInternalNotesChange={setInternalNotes}
          onCustomerNotesChange={setCustomerNotes}
          disabled={isTerminal}
        />
      </div>

      {/* Status Actions */}
      <div className="flex justify-end">
        <OrderStatusActions
          currentStatus={status}
          onTransition={(target) => transitionMutation.mutate(target)}
          isLoading={transitionMutation.isPending}
        />
      </div>
    </div>
  )
}
