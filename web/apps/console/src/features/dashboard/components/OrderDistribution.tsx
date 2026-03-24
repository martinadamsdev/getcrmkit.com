import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@workspace/ui/components/card";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from "recharts";

import type { OrderDistributionItem } from "../types";

interface OrderDistributionProps {
  data: OrderDistributionItem[];
}

const STATUS_LABELS: Record<string, string> = {
  confirmed: "已确认",
  shipped: "已发货",
  delivered: "已交付",
  cancelled: "已取消",
};

const COLORS = [
  "oklch(0.55 0.19 255)", // blue
  "oklch(0.65 0.17 155)", // green
  "oklch(0.75 0.15 75)", // amber
  "oklch(0.60 0.20 25)", // red
  "oklch(0.55 0.15 300)", // purple
];

export function OrderDistribution({ data }: OrderDistributionProps) {
  const chartData = data.map((item) => ({
    name: STATUS_LABELS[item.status] ?? item.status,
    value: item.count,
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">订单分布</CardTitle>
      </CardHeader>
      <CardContent>
        {data.length === 0 ? (
          <p className="py-8 text-center text-sm text-muted-foreground">
            暂无数据
          </p>
        ) : (
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                innerRadius={50}
                outerRadius={80}
                dataKey="value"
                paddingAngle={2}
              >
                {chartData.map((_, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        )}
      </CardContent>
    </Card>
  );
}
