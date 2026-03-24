import { Download } from "lucide-react";
import { Button } from "@workspace/ui/components/button";
import {
  ToggleGroup,
  ToggleGroupItem,
} from "@workspace/ui/components/toggle-group";

export type ReportPeriod = "daily" | "weekly" | "monthly" | "yearly";

const PERIOD_LABELS: Record<ReportPeriod, string> = {
  daily: "日报",
  weekly: "周报",
  monthly: "月报",
  yearly: "年报",
};

interface ReportButtonsProps {
  period: ReportPeriod;
  onPeriodChange: (period: ReportPeriod) => void;
  onExport: () => void;
  exporting?: boolean;
}

export function ReportButtons({
  period,
  onPeriodChange,
  onExport,
  exporting = false,
}: ReportButtonsProps) {
  return (
    <div className="flex items-center gap-2">
      <ToggleGroup
        type="single"
        value={period}
        onValueChange={(val) => {
          if (val) onPeriodChange(val as ReportPeriod);
        }}
      >
        {(
          Object.entries(PERIOD_LABELS) as [ReportPeriod, string][]
        ).map(([value, label]) => (
          <ToggleGroupItem key={value} value={value} size="sm">
            {label}
          </ToggleGroupItem>
        ))}
      </ToggleGroup>
      <Button
        variant="outline"
        size="sm"
        onClick={onExport}
        disabled={exporting}
        aria-label="导出"
      >
        <Download className="mr-1.5 h-3.5 w-3.5" />
        {exporting ? "导出中..." : "导出"}
      </Button>
    </div>
  );
}
