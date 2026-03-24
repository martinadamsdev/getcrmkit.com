import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@workspace/ui/components/card";

interface SalesSummaryProps {
  yearlySalesUsd: number;
  monthlySalesUsd: number;
}

function formatUsd(amount: number): string {
  return `$${amount.toLocaleString("en-US")}`;
}

export function SalesSummary({
  yearlySalesUsd,
  monthlySalesUsd,
}: SalesSummaryProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">年度销售额</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-4xl font-bold">{formatUsd(yearlySalesUsd)}</p>
        <div>
          <p className="text-xs text-muted-foreground">本月销售额</p>
          <p className="text-xl font-semibold">{formatUsd(monthlySalesUsd)}</p>
        </div>
      </CardContent>
    </Card>
  );
}
