import { useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@workspace/ui/components/resizable";
import { FollowUpToolbar } from "@/features/follow-up/components/follow-up-toolbar";
import { FollowUpFilters } from "@/features/follow-up/components/follow-up-filters";
import { FollowUpTable } from "@/features/follow-up/components/follow-up-table";
import { FollowUpCreateDialog } from "@/features/follow-up/components/follow-up-create-dialog";
import { ReportButtons } from "@/features/follow-up/components/report-buttons";
import type { ReportPeriod } from "@/features/follow-up/components/report-buttons";
import { ScriptTemplatePanel } from "@/features/follow-up/components/script-template-panel";
import { useFollowUpExport } from "@/features/follow-up/hooks/use-follow-up-export";
import { PageHeader } from "@/shared/components/layout/page-header";
import { apiFetch } from "@/shared/api/fetcher";

export const Route = createFileRoute("/_app/follow-ups/")({
  component: FollowUpsPage,
});

interface FollowUpListResponse {
  items: Array<{
    id: string;
    customer_id: string;
    contact_id: string | null;
    method: string;
    stage: string | null;
    content: string;
    customer_response: string | null;
    next_follow_at: string | null;
    attachment_urls: string[];
    tags: string[];
    created_by: string | null;
    created_at: string;
    updated_at: string;
  }>;
  total: number;
  page: number;
  page_size: number;
}

async function fetchFollowUps(params: {
  page: number;
  pageSize: number;
  method?: string;
  tags?: string[];
}): Promise<FollowUpListResponse> {
  const searchParams = new URLSearchParams();
  searchParams.set("page", String(params.page));
  searchParams.set("page_size", String(params.pageSize));
  if (params.method) searchParams.set("method", params.method);
  if (params.tags?.length) {
    for (const tag of params.tags) {
      searchParams.append("tags", tag);
    }
  }
  const res = await apiFetch(`/api/v1/follow-ups?${searchParams}`);
  if (!res.ok) throw new Error("Failed to fetch follow-ups");
  return res.json();
}

function FollowUpsPage() {
  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);
  const [filtersOpen, setFiltersOpen] = useState(false);
  const [methodFilter, setMethodFilter] = useState<string | undefined>();
  const [createOpen, setCreateOpen] = useState(false);
  const [reportPeriod, setReportPeriod] = useState<ReportPeriod>("daily");
  const { exportReport, exporting } = useFollowUpExport();

  const { data, isLoading } = useQuery({
    queryKey: ["follow-ups", { page, pageSize, method: methodFilter }],
    queryFn: () =>
      fetchFollowUps({ page, pageSize, method: methodFilter }),
    staleTime: 30_000,
  });

  // TODO: Enrich items with customer_name via a join or separate lookup
  const enrichedItems =
    data?.items.map((item) => ({
      ...item,
      customer_name: `客户 ${item.customer_id.slice(0, 6)}...`, // TODO: backend should join customer_name
    })) ?? [];

  return (
    <div className="flex h-full flex-col">
      <PageHeader
        title="跟进记录"
        description="管理客户跟进和话术模板"
        actions={
          <ReportButtons
            period={reportPeriod}
            onPeriodChange={setReportPeriod}
            onExport={() => exportReport(reportPeriod)}
            exporting={exporting}
          />
        }
      />

      <ResizablePanelGroup direction="horizontal" className="flex-1">
        <ResizablePanel defaultSize={75} minSize={50}>
          <div className="flex h-full flex-col">
            <FollowUpToolbar
              onSearch={() => {}}
              onCreateClick={() => setCreateOpen(true)}
              onFilterToggle={() => setFiltersOpen(!filtersOpen)}
              filtersOpen={filtersOpen}
            />
            {filtersOpen && (
              <FollowUpFilters
                method={methodFilter}
                onMethodChange={(m) => {
                  setMethodFilter(m);
                  setPage(1);
                }}
                onReset={() => {
                  setMethodFilter(undefined);
                  setPage(1);
                }}
              />
            )}
            <div className="flex-1 overflow-auto">
              {isLoading ? (
                <div className="flex h-48 items-center justify-center text-muted-foreground">
                  加载中...
                </div>
              ) : (
                <FollowUpTable
                  data={enrichedItems}
                  total={data?.total ?? 0}
                  page={page}
                  pageSize={pageSize}
                  onPageChange={setPage}
                />
              )}
            </div>
          </div>
        </ResizablePanel>

        <ResizableHandle withHandle />

        <ResizablePanel defaultSize={25} minSize={20} maxSize={40}>
          <ScriptTemplatePanel />
        </ResizablePanel>
      </ResizablePanelGroup>

      <FollowUpCreateDialog
        open={createOpen}
        onOpenChange={setCreateOpen}
      />
    </div>
  );
}
