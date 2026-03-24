import { Link } from "@tanstack/react-router";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@workspace/ui/components/card";
import { Badge } from "@workspace/ui/components/badge";
import { Truck } from "lucide-react";

import type { DeliveryAlert } from "../types";

interface DeliveryAlertPanelProps {
  alerts: DeliveryAlert[];
}

export function DeliveryAlertPanel({ alerts }: DeliveryAlertPanelProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <Truck className="h-4 w-4" />
          发货预警
        </CardTitle>
      </CardHeader>
      <CardContent>
        {alerts.length === 0 ? (
          <p className="py-4 text-center text-sm text-muted-foreground">
            无发货预警
          </p>
        ) : (
          <div className="space-y-3">
            {alerts.map((alert) => (
              <Link
                key={alert.order_id}
                to="/orders/$id"
                params={{ id: alert.order_id }}
                className="flex items-center justify-between rounded-md p-2 transition-colors hover:bg-secondary/50"
              >
                <div>
                  <p className="text-sm font-medium">{alert.order_number}</p>
                  <p className="text-xs text-muted-foreground">
                    {alert.customer_name}
                  </p>
                </div>
                <Badge
                  variant={
                    alert.status === "overdue" ? "destructive" : "outline"
                  }
                >
                  {alert.status === "overdue" ? "逾期" : "7天内到期"}
                </Badge>
              </Link>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
