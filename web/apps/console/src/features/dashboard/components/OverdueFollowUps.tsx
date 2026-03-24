import { Link } from "@tanstack/react-router";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@workspace/ui/components/card";
import { MessageSquare } from "lucide-react";

import type { OverdueFollowUp } from "../types";

interface OverdueFollowUpsProps {
  followUps: OverdueFollowUp[];
}

export function OverdueFollowUps({ followUps }: OverdueFollowUpsProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <MessageSquare className="h-4 w-4" />
          超期跟进
        </CardTitle>
      </CardHeader>
      <CardContent>
        {followUps.length === 0 ? (
          <p className="py-4 text-center text-sm text-muted-foreground">
            所有客户都已跟进
          </p>
        ) : (
          <div className="space-y-3">
            {followUps.map((item) => (
              <Link
                key={item.customer_id}
                to="/customers/$id"
                params={{ id: item.customer_id }}
                className="flex items-center justify-between rounded-md p-2 transition-colors hover:bg-secondary/50"
              >
                <div className="flex items-center gap-2">
                  <span className="h-2 w-2 rounded-full bg-destructive" />
                  <span className="text-sm font-medium">
                    {item.customer_name}
                  </span>
                </div>
                <span className="text-xs font-medium text-destructive">
                  {item.days_since_last_follow_up}天未跟进
                </span>
              </Link>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
