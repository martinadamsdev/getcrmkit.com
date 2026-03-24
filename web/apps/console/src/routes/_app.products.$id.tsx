import { createFileRoute, Link } from "@tanstack/react-router"
import { useQuery, useQueryClient } from "@tanstack/react-query"
import { ArrowLeft } from "lucide-react"
import { Button } from "@workspace/ui/components/button"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@workspace/ui/components/card"
import { Badge } from "@workspace/ui/components/badge"
import { Separator } from "@workspace/ui/components/separator"
import { toast } from "sonner"
import { VariantTable } from "@/features/product/components/variant-table"
import { PricingTierTable } from "@/features/product/components/pricing-tier-table"
import { CustomizationOptionList } from "@/features/product/components/customization-option-list"
import { PageHeader } from "@/shared/components/layout/page-header"
import { apiFetch } from "@/shared/api/fetcher"

export const Route = createFileRoute("/_app/products/$id")({
  component: ProductDetailPage,
})

interface ProductDetail {
  id: string
  name: string
  sku: string | null
  description: string | null
  image_url: string | null
  category_name: string | null
  material: string | null
  dimensions: string | null
  weight: string | null
  color: string | null
  packing: string | null
  cost_price: string | null
  cost_currency: string
  selling_price: string | null
  selling_currency: string
  is_active: boolean
  variants: Array<{
    id: string
    material: string | null
    color: string | null
    color_name: string | null
    size: string | null
    sku: string | null
    cost_price: string | null
  }>
  pricing_tiers: Array<{
    id: string
    min_qty: number
    max_qty: number | null
    multiplier: string
  }>
  customization_options: Array<{
    id: string
    name: string
    surcharge: string
  }>
}

async function fetchProduct(id: string): Promise<ProductDetail> {
  const res = await apiFetch(`/api/v1/products/${id}`)
  if (!res.ok) throw new Error("Product not found")
  return res.json()
}

function ProductDetailPage() {
  const { id } = Route.useParams()
  const queryClient = useQueryClient()

  const {
    data: product,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["product", id],
    queryFn: () => fetchProduct(id),
    staleTime: 30_000,
  })

  const handleAddVariant = async () => {
    const res = await apiFetch(`/api/v1/products/${id}/variants`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ material: "", color: null, size: "", sku: "" }),
    })
    if (res.ok) {
      queryClient.invalidateQueries({ queryKey: ["product", id] })
      toast.success("变体已添加")
    }
  }

  const handleUpdateVariant = async (
    variantId: string,
    field: string,
    value: string,
  ) => {
    await apiFetch(`/api/v1/products/${id}/variants/${variantId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ [field]: value || null }),
    })
    queryClient.invalidateQueries({ queryKey: ["product", id] })
  }

  const handleDeleteVariant = async (variantId: string) => {
    await apiFetch(`/api/v1/products/${id}/variants/${variantId}`, {
      method: "DELETE",
    })
    queryClient.invalidateQueries({ queryKey: ["product", id] })
    toast.success("变体已删除")
  }

  const handleAddTier = () => {
    toast.info("添加阶梯定价（待实现）")
  }

  const handleUpdateTier = (_tierId: string, _field: string, _value: string) => {
    toast.info("阶梯定价编辑功能开发中") // TODO: PUT tier update then invalidate
  }

  const handleDeleteTier = (_tierId: string) => {
    toast.info("阶梯定价删除功能开发中") // TODO: DELETE tier then invalidate
  }

  const handleAddOption = () => {
    toast.info("添加定制选项（待实现）")
  }

  const handleUpdateOption = (_optId: string, _field: string, _value: string) => {
    toast.info("定制选项编辑功能开发中") // TODO: PUT option update
  }

  const handleDeleteOption = (_optId: string) => {
    toast.info("定制选项删除功能开发中") // TODO: DELETE option
  }

  if (isLoading) {
    return (
      <div className="flex h-48 items-center justify-center text-muted-foreground">
        加载中...
      </div>
    )
  }

  if (error || !product) {
    return (
      <div className="flex h-48 flex-col items-center justify-center gap-2 text-muted-foreground">
        <p>产品未找到</p>
        <Link to="/products">
          <Button variant="outline" size="sm">
            <ArrowLeft className="mr-1.5 h-3.5 w-3.5" />
            返回列表
          </Button>
        </Link>
      </div>
    )
  }

  return (
    <div className="flex h-full flex-col">
      <PageHeader
        title={product.name}
        description={product.sku ? `SKU: ${product.sku}` : undefined}
        actions={
          <div className="flex items-center gap-2">
            <Badge variant={product.is_active ? "default" : "secondary"}>
              {product.is_active ? "在售" : "下架"}
            </Badge>
            <Link to="/products">
              <Button variant="outline" size="sm">
                <ArrowLeft className="mr-1.5 h-3.5 w-3.5" />
                返回
              </Button>
            </Link>
          </div>
        }
      />

      <div className="flex-1 overflow-auto">
        <div className="space-y-6 p-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">基本信息</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-muted-foreground">分类:</span>{" "}
                  {product.category_name ?? "未分类"}
                </div>
                <div>
                  <span className="text-muted-foreground">材质:</span>{" "}
                  {product.material ?? "\u2014"}
                </div>
                <div>
                  <span className="text-muted-foreground">尺寸:</span>{" "}
                  {product.dimensions ?? "\u2014"}
                </div>
                <div>
                  <span className="text-muted-foreground">重量:</span>{" "}
                  {product.weight ? `${product.weight}kg` : "\u2014"}
                </div>
                <div>
                  <span className="text-muted-foreground">成本:</span>{" "}
                  {product.cost_price ? `\u00a5${product.cost_price}` : "\u2014"}
                </div>
                <div>
                  <span className="text-muted-foreground">售价:</span>{" "}
                  {product.selling_price
                    ? `$${product.selling_price}`
                    : "\u2014"}
                </div>
              </div>
              {product.description && (
                <>
                  <Separator className="my-4" />
                  <p className="text-sm text-muted-foreground">
                    {product.description}
                  </p>
                </>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <VariantTable
                variants={product.variants}
                onAdd={handleAddVariant}
                onUpdate={handleUpdateVariant}
                onDelete={handleDeleteVariant}
              />
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <PricingTierTable
                tiers={product.pricing_tiers}
                onAdd={handleAddTier}
                onUpdate={handleUpdateTier}
                onDelete={handleDeleteTier}
              />
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <CustomizationOptionList
                options={product.customization_options}
                onAdd={handleAddOption}
                onUpdate={handleUpdateOption}
                onDelete={handleDeleteOption}
              />
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
