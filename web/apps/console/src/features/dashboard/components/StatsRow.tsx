import { useNavigate } from "@tanstack/react-router";
import {
  Users,
  FileText,
  ShoppingCart,
  MessageSquare,
  Truck,
} from "lucide-react";
import { Badge } from "@workspace/ui/components/badge";

import { StatCard } from "../../../shared/components/data/StatCard";
import type { DashboardStats } from "../types";

interface StatsRowProps {
  stats: DashboardStats;
}

export function StatsRow({ stats }: StatsRowProps) {
  const navigate = useNavigate();

  return (
    <div className="grid grid-cols-5 gap-4" data-testid="stats-row">
      <StatCard
        title="客户总数"
        value={stats.total_customers}
        icon={<Users className="h-5 w-5" />}
        onClick={() => navigate({ to: "/customers" })}
      />
      <StatCard
        title="报价单"
        value={stats.total_quotations}
        subtitle={`转化率 ${stats.quotation_conversion_rate}%`}
        icon={<FileText className="h-5 w-5" />}
        onClick={() => navigate({ to: "/quotations" })}
      />
      <StatCard
        title="成交订单"
        value={stats.total_orders}
        icon={<ShoppingCart className="h-5 w-5" />}
        onClick={() => navigate({ to: "/orders" })}
      />
      <div className="relative">
        <StatCard
          title="待跟进"
          value={stats.pending_follow_ups}
          icon={<MessageSquare className="h-5 w-5" />}
          onClick={() => navigate({ to: "/follow-ups" })}
        />
        {stats.pending_follow_ups > 0 && (
          <Badge
            variant="destructive"
            className="absolute right-3 top-3 text-xs"
          >
            超15天
          </Badge>
        )}
      </div>
      <StatCard
        title="发货预警"
        value={stats.delivery_alerts}
        icon={<Truck className="h-5 w-5" />}
        onClick={() => navigate({ to: "/orders" })}
      />
    </div>
  );
}
