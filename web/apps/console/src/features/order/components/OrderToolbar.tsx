import { SearchInput } from "@/shared/components/form/search-input"
import { OrderStatusFilter } from "./OrderStatusFilter"
import { PaymentStatusFilter } from "./PaymentStatusFilter"
import type { OrderStatus, PaymentStatus } from "@/shared/lib/constants"

interface OrderToolbarProps {
  search: string
  onSearchChange: (value: string) => void
  orderStatus: OrderStatus | null
  onOrderStatusChange: (status: OrderStatus | null) => void
  paymentStatus: PaymentStatus | null
  onPaymentStatusChange: (status: PaymentStatus | null) => void
}

export function OrderToolbar({
  search,
  onSearchChange,
  orderStatus,
  onOrderStatusChange,
  paymentStatus,
  onPaymentStatusChange,
}: OrderToolbarProps) {
  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <SearchInput
          placeholder="搜索订单编号、客户..."
          defaultValue={search}
          onSearch={onSearchChange}
          className="w-80"
        />
      </div>
      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-2">
          <span className="whitespace-nowrap text-xs font-medium text-muted-foreground">
            订单状态
          </span>
          <OrderStatusFilter
            value={orderStatus}
            onChange={onOrderStatusChange}
          />
        </div>
        <div className="flex items-center gap-2">
          <span className="whitespace-nowrap text-xs font-medium text-muted-foreground">
            付款状态
          </span>
          <PaymentStatusFilter
            value={paymentStatus}
            onChange={onPaymentStatusChange}
          />
        </div>
      </div>
    </div>
  )
}
