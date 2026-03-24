import { Link } from "@tanstack/react-router";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@workspace/ui/components/card";
import { Button } from "@workspace/ui/components/button";
import { Badge } from "@workspace/ui/components/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@workspace/ui/components/table";

import type { RecentOrder } from "../types";

interface RecentOrdersProps {
  orders: RecentOrder[];
}

function formatMoney(amount: number, currency: string): string {
  const symbol = currency === "USD" ? "$" : currency === "CNY" ? "\u00a5" : currency;
  return `${symbol}${amount.toLocaleString("en-US")}`;
}

export function RecentOrders({ orders }: RecentOrdersProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-base">最近订单</CardTitle>
        <Link to="/orders">
          <Button variant="ghost" size="sm">
            全部
          </Button>
        </Link>
      </CardHeader>
      <CardContent>
        {orders.length === 0 ? (
          <div className="py-6 text-center">
            <p className="text-sm text-muted-foreground">暂无订单</p>
            <Link to="/orders">
              <Button variant="outline" size="sm" className="mt-2">
                创建第一个订单
              </Button>
            </Link>
          </div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>订单号</TableHead>
                <TableHead>客户</TableHead>
                <TableHead className="text-right">金额</TableHead>
                <TableHead>状态</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {orders.map((o) => (
                <TableRow key={o.id}>
                  <TableCell className="text-sm font-medium">
                    {o.order_number}
                  </TableCell>
                  <TableCell className="text-sm">{o.customer_name}</TableCell>
                  <TableCell className="text-right text-sm">
                    {formatMoney(o.amount, o.currency)}
                  </TableCell>
                  <TableCell>
                    <Badge variant="secondary">{o.status}</Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  );
}
