import { useState } from "react";
import { toast } from "sonner";
import type { ReportPeriod } from "../components/report-buttons";

export function useFollowUpExport() {
  const [exporting, setExporting] = useState(false);

  const exportReport = async (period: ReportPeriod) => {
    setExporting(true);
    try {
      const res = await fetch(
        `/api/v1/follow-ups/report/export?period=${period}`,
      );
      if (!res.ok) throw new Error("Export failed");
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `follow-up-report-${period}.xlsx`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(() => URL.revokeObjectURL(url), 100);
      toast.success("导出成功");
    } catch {
      toast.error("导出失败，请重试");
    } finally {
      setExporting(false);
    }
  };

  return { exportReport, exporting };
}
