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

import type { RecentQuotation } from "../types";

interface RecentQuotationsProps {
  quotations: RecentQuotation[];
}

function formatMoney(amount: number, currency: string): string {
  const symbol = currency === "USD" ? "$" : currency === "CNY" ? "\u00a5" : currency;
  return `${symbol}${amount.toLocaleString("en-US")}`;
}

export function RecentQuotations({ quotations }: RecentQuotationsProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-base">最近报价</CardTitle>
        <Link to="/quotations">
          <Button variant="ghost" size="sm">
            全部
          </Button>
        </Link>
      </CardHeader>
      <CardContent>
        {quotations.length === 0 ? (
          <div className="py-6 text-center">
            <p className="text-sm text-muted-foreground">暂无报价</p>
            <Link to="/quotations/new">
              <Button variant="outline" size="sm" className="mt-2">
                创建第一个报价
              </Button>
            </Link>
          </div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>客户</TableHead>
                <TableHead>产品</TableHead>
                <TableHead className="text-right">金额</TableHead>
                <TableHead>状态</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {quotations.map((q) => (
                <TableRow key={q.id}>
                  <TableCell className="text-sm">{q.customer_name}</TableCell>
                  <TableCell className="text-sm">{q.product_name}</TableCell>
                  <TableCell className="text-right text-sm">
                    {formatMoney(q.amount, q.currency)}
                  </TableCell>
                  <TableCell>
                    <Badge variant="secondary">{q.status}</Badge>
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
