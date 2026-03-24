import { useState } from "react"
import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { useQuery, useQueryClient } from "@tanstack/react-query"
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@workspace/ui/components/resizable"
import { ScrollArea } from "@workspace/ui/components/scroll-area"
import { Button } from "@workspace/ui/components/button"
import { Plus } from "lucide-react"
import { toast } from "sonner"
import { CategoryTree } from "@/features/product/components/category-tree"
import { ProductToolbar } from "@/features/product/components/product-toolbar"
import { ProductTable } from "@/features/product/components/product-table"
import { ProductCreateDialog } from "@/features/product/components/product-create-dialog"
import { ImportDialog } from "@/shared/components/business/import-dialog"
import { PageHeader } from "@/shared/components/layout/page-header"
import { apiFetch } from "@/shared/api/fetcher"

const PRODUCT_SYSTEM_FIELDS = [
  { key: "name", label: "产品名称", required: true },
  { key: "sku", label: "SKU" },
  { key: "category_name", label: "分类" },
  { key: "material", label: "材质" },
  { key: "dimensions", label: "尺寸" },
  { key: "weight", label: "重量" },
  { key: "color", label: "颜色" },
  { key: "packing", label: "包装" },
  { key: "cost_price", label: "成本价" },
  { key: "cost_currency", label: "成本币种" },
  { key: "selling_price", label: "售价" },
  { key: "selling_currency", label: "售价币种" },
  { key: "description", label: "描述" },
]

export const Route = createFileRoute("/_app/products/")({
  component: ProductsPage,
})

interface CategoryNode {
  id: string
  name: string
  parent_id: string | null
  level: number
  position: number
  product_count: number
  children: CategoryNode[]
}

async function fetchCategories(): Promise<CategoryNode[]> {
  const res = await apiFetch("/api/v1/product-categories")
  if (!res.ok) return []
  return res.json()
}

async function fetchProducts(params: {
  page: number
  pageSize: number
  keyword?: string
  categoryId?: string
}) {
  const searchParams = new URLSearchParams()
  searchParams.set("page", String(params.page))
  searchParams.set("page_size", String(params.pageSize))
  if (params.keyword) searchParams.set("keyword", params.keyword)
  if (params.categoryId) searchParams.set("category_id", params.categoryId)
  const res = await apiFetch(`/api/v1/products?${searchParams}`)
  if (!res.ok) throw new Error("Failed to fetch products")
  return res.json()
}

async function exportProducts() {
  const res = await apiFetch("/api/v1/products/export")
  if (!res.ok) throw new Error("Export failed")
  const blob = await res.blob()
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = "products.xlsx"
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  setTimeout(() => URL.revokeObjectURL(url), 100)
}

function ProductsPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const [page, setPage] = useState(1)
  const [pageSize] = useState(20)
  const [keyword, setKeyword] = useState("")
  const [selectedCategoryId, setSelectedCategoryId] = useState<string | null>(
    null,
  )
  const [createOpen, setCreateOpen] = useState(false)
  const [importOpen, setImportOpen] = useState(false)

  const { data: categories = [] } = useQuery({
    queryKey: ["product-categories"],
    queryFn: fetchCategories,
    staleTime: 60_000,
  })

  const { data: productData, isLoading } = useQuery({
    queryKey: [
      "products",
      { page, pageSize, keyword, categoryId: selectedCategoryId },
    ],
    queryFn: () =>
      fetchProducts({
        page,
        pageSize,
        keyword: keyword || undefined,
        categoryId: selectedCategoryId ?? undefined,
      }),
    staleTime: 30_000,
  })

  const handleReorder = async (
    items: { id: string; position: number }[],
  ) => {
    try {
      await Promise.all(
        items.map((item) =>
          apiFetch(`/api/v1/product-categories/${item.id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ position: item.position }),
          }),
        ),
      )
      queryClient.invalidateQueries({ queryKey: ["product-categories"] })
    } catch {
      toast.error("排序保存失败")
      queryClient.invalidateQueries({ queryKey: ["product-categories"] })
    }
  }

  const handleExport = async () => {
    try {
      await exportProducts()
      toast.success("导出成功")
    } catch {
      toast.error("导出失败")
    }
  }

  return (
    <div className="flex h-full flex-col">
      <PageHeader title="产品管理" description="管理产品、变体和定价" />

      <ResizablePanelGroup orientation="horizontal" className="flex-1">
        <ResizablePanel defaultSize={20} minSize={15} maxSize={30}>
          <div className="flex h-full flex-col border-r">
            <div className="flex items-center justify-between border-b px-3 py-2">
              <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                产品分类
              </h3>
              <Button variant="ghost" size="icon" className="h-6 w-6">
                <Plus className="h-3.5 w-3.5" />
              </Button>
            </div>
            <ScrollArea className="flex-1 px-2 py-2">
              <button
                type="button"
                className={`mb-1 w-full rounded px-2 py-1.5 text-left text-sm ${
                  selectedCategoryId === null
                    ? "bg-accent text-accent-foreground"
                    : "hover:bg-accent/50"
                }`}
                onClick={() => {
                  setSelectedCategoryId(null)
                  setPage(1)
                }}
              >
                全部产品
              </button>
              <CategoryTree
                categories={categories}
                selectedId={selectedCategoryId}
                onSelect={(id) => {
                  setSelectedCategoryId(id)
                  setPage(1)
                }}
                onReorder={handleReorder}
              />
            </ScrollArea>
          </div>
        </ResizablePanel>

        <ResizableHandle />

        <ResizablePanel defaultSize={80} minSize={50}>
          <div className="flex h-full flex-col">
            <ProductToolbar
              onSearch={(q) => {
                setKeyword(q)
                setPage(1)
              }}
              onCreateClick={() => setCreateOpen(true)}
              onImportClick={() => setImportOpen(true)}
              onExportClick={handleExport}
            />
            <div className="flex-1 overflow-auto">
              {isLoading ? (
                <div className="flex h-48 items-center justify-center text-muted-foreground">
                  加载中...
                </div>
              ) : (
                <ProductTable
                  data={productData?.items ?? []}
                  total={productData?.total ?? 0}
                  page={page}
                  pageSize={pageSize}
                  onPageChange={setPage}
                  onRowClick={(id) =>
                    navigate({ to: "/products/$id", params: { id } })
                  }
                />
              )}
            </div>
          </div>
        </ResizablePanel>
      </ResizablePanelGroup>

      <ProductCreateDialog open={createOpen} onOpenChange={setCreateOpen} />

      <ImportDialog
        open={importOpen}
        onOpenChange={setImportOpen}
        entityType="product"
        uploadEndpoint="/api/v1/products/import"
        systemFields={PRODUCT_SYSTEM_FIELDS}
        onComplete={() => {
          queryClient.invalidateQueries({ queryKey: ["products"] })
          toast.success("产品导入完成")
        }}
      />
    </div>
  )
}
