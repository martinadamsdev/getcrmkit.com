import { useState } from "react"
import { createFileRoute } from "@tanstack/react-router"
import { useQuery, useQueryClient } from "@tanstack/react-query"
import { parseAsString, useQueryState } from "nuqs"
import { Plus } from "lucide-react"
import { Button } from "@workspace/ui/components/button"
import { PageContainer } from "@/shared/components/layout/page-container"
import { PageHeader } from "@/shared/components/layout/page-header"
import { usePagination } from "@/shared/hooks/use-pagination"
import { useFilters, type FilterDef } from "@/shared/hooks/use-filters"
import { CustomerToolbar } from "@/features/customer/components/customer-toolbar"
import { CustomerFilterPanel } from "@/features/customer/components/customer-filter-panel"
import { SavedViewTabs } from "@/features/customer/components/saved-view-tabs"
import { CustomerTable } from "@/features/customer/components/customer-table"
import { CustomerCreateDialog } from "@/features/customer/components/customer-create-dialog"
import { ImportDialog } from "@/shared/components/business/import-dialog"
import { apiFetch } from "@/shared/api/fetcher"

export const Route = createFileRoute("/_app/customers/")({
  component: CustomerListPage,
})

const customerFilterDefs: FilterDef[] = [
  {
    key: "grade_id",
    label: "客户等级",
    type: "select",
    options: [
      { label: "A", value: "A" },
      { label: "B", value: "B" },
      { label: "C", value: "C" },
      { label: "D", value: "D" },
    ],
  },
  {
    key: "source",
    label: "来源",
    type: "select",
    options: [
      { label: "阿里巴巴", value: "alibaba" },
      { label: "展会", value: "exhibition" },
      { label: "推荐", value: "referral" },
      { label: "网站", value: "website" },
      { label: "LinkedIn", value: "linkedin" },
      { label: "其他", value: "other" },
    ],
  },
  { key: "country", label: "国家", type: "text" },
  { key: "industry", label: "行业", type: "text" },
  {
    key: "follow_status",
    label: "跟进状态",
    type: "select",
    options: [
      { label: "新客户", value: "new" },
      { label: "已联系", value: "contacted" },
      { label: "已报价", value: "quoted" },
      { label: "已寄样", value: "sample_sent" },
      { label: "谈判中", value: "negotiating" },
      { label: "已下单", value: "ordered" },
      { label: "已流失", value: "lost" },
    ],
  },
]

const CUSTOMER_SYSTEM_FIELDS = [
  { key: "name", label: "客户名称", required: true },
  { key: "country", label: "国家" },
  { key: "email", label: "邮箱" },
  { key: "phone", label: "电话" },
  { key: "industry", label: "行业" },
  { key: "source", label: "来源" },
  { key: "address", label: "地址" },
  { key: "website", label: "网站" },
  { key: "remark", label: "备注" },
]

async function fetchCustomers(params: Record<string, string | number | null>) {
  const searchParams = new URLSearchParams()
  for (const [key, value] of Object.entries(params)) {
    if (value != null && value !== "") {
      searchParams.set(key, String(value))
    }
  }
  const res = await apiFetch(`/api/v1/customers?${searchParams}`)
  if (!res.ok) throw new Error("Failed to fetch customers")
  return res.json()
}

function CustomerListPage() {
  const queryClient = useQueryClient()
  const { page, pageSize, setPage } = usePagination()
  const { filters, setFilter, resetFilters } = useFilters(customerFilterDefs)
  const [keyword, setKeyword] = useQueryState("q", parseAsString.withDefault(""))
  const [sorting, setSorting] = useState<{ id: string; desc: boolean }[]>([])
  const [createDialogOpen, setCreateDialogOpen] = useState(false)
  const [importDialogOpen, setImportDialogOpen] = useState(false)
  const [filterPanelOpen, setFilterPanelOpen] = useState(false)

  const activeFilterCount = Object.values(filters).filter(
    (v) => v != null && v !== "",
  ).length

  const sortParam = sorting[0]
    ? `${sorting[0].desc ? "-" : ""}${sorting[0].id}`
    : undefined

  const customersQuery = useQuery({
    queryKey: ["customers", { page, pageSize, keyword, ...filters, sort: sortParam }],
    queryFn: () =>
      fetchCustomers({
        page,
        page_size: pageSize,
        keyword: keyword || null,
        sort: sortParam ?? null,
        ...filters,
      }),
  })

  const handleViewChange = (viewFilters: Record<string, string | null>) => {
    for (const [key, value] of Object.entries(viewFilters)) {
      setFilter(key, value)
    }
  }

  return (
    <PageContainer>
      <PageHeader
        title="客户管理"
        description="管理你的客户信息"
        actions={
          <Button onClick={() => setCreateDialogOpen(true)}>
            <Plus className="mr-1 size-4" />
            新建客户
          </Button>
        }
      />

      <SavedViewTabs
        views={[]}
        onViewChange={handleViewChange}
        onSave={(name) => { /* TODO: POST /saved-views */ }}
        onDelete={(id) => { /* TODO: DELETE /saved-views/{id} */ }}
      />

      <CustomerToolbar
        onSearch={setKeyword}
        onFilterClick={() => setFilterPanelOpen((prev) => !prev)}
        activeFilterCount={activeFilterCount}
        defaultSearchValue={keyword}
        onCreateClick={() => setCreateDialogOpen(true)}
        onImportClick={() => setImportDialogOpen(true)}
      />

      {filterPanelOpen && (
        <CustomerFilterPanel
          filters={filters}
          onChange={setFilter}
          onReset={resetFilters}
        />
      )}

      <CustomerTable
        data={customersQuery.data?.items ?? []}
        pagination={{
          page,
          pageSize,
          total: customersQuery.data?.total ?? 0,
        }}
        onPageChange={setPage}
        sorting={sorting}
        onSortingChange={setSorting}
        isLoading={customersQuery.isLoading}
      />

      <CustomerCreateDialog
        open={createDialogOpen}
        onOpenChange={setCreateDialogOpen}
        onSubmit={async (data) => {
          await apiFetch("/api/v1/customers", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
          })
          setCreateDialogOpen(false)
          queryClient.invalidateQueries({ queryKey: ["customers"] })
        }}
        onCheckDuplicate={async (name) => {
          const res = await apiFetch("/api/v1/customers/check-duplicate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ company_name: name }),
          })
          return res.ok ? ((await res.json()).duplicates ?? []) : []
        }}
      />

      <ImportDialog
        open={importDialogOpen}
        onOpenChange={setImportDialogOpen}
        entityType="customer"
        uploadEndpoint="/api/v1/customers/import"
        systemFields={CUSTOMER_SYSTEM_FIELDS}
        onComplete={() => customersQuery.refetch()}
      />
    </PageContainer>
  )
}
