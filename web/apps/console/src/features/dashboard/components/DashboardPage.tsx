import { Button } from "@workspace/ui/components/button";
import { useDashboard } from "../hooks/useDashboard";
import { DashboardSkeleton } from "./DashboardSkeleton";
import { StatsRow } from "./StatsRow";
import { SalesSummary } from "./SalesSummary";
import { DeliveryAlertPanel } from "./DeliveryAlertPanel";
import { RecentQuotations } from "./RecentQuotations";
import { OverdueFollowUps } from "./OverdueFollowUps";
import { OrderDistribution } from "./OrderDistribution";
import { RecentOrders } from "./RecentOrders";

export function DashboardPage() {
  const { data, isLoading, isError } = useDashboard();

  if (isLoading) {
    return <DashboardSkeleton />;
  }

  if (isError || !data) {
    return (
      <div className="flex flex-col items-center justify-center h-64 gap-4">
        <p className="text-muted-foreground">加载失败</p>
        <Button onClick={() => window.location.reload()}>重试</Button>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      {/* Row 1: 5 StatCards */}
      <StatsRow stats={data.stats} />

      {/* Row 2: SalesSummary + DeliveryAlertPanel */}
      <div className="grid grid-cols-2 gap-4">
        <SalesSummary
          yearlySalesUsd={data.sales_summary.yearly_sales_usd}
          monthlySalesUsd={data.sales_summary.monthly_sales_usd}
        />
        <DeliveryAlertPanel alerts={data.delivery_alerts} />
      </div>

      {/* Row 3: RecentQuotations + OverdueFollowUps */}
      <div className="grid grid-cols-2 gap-4">
        <RecentQuotations quotations={data.recent_quotations} />
        <OverdueFollowUps followUps={data.overdue_follow_ups} />
      </div>

      {/* Row 4: OrderDistribution + RecentOrders */}
      <div className="grid grid-cols-2 gap-4">
        <OrderDistribution data={data.order_distribution} />
        <RecentOrders orders={data.recent_orders} />
      </div>
    </div>
  );
}
