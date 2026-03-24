import { useState } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { Button } from "@workspace/ui/components/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@workspace/ui/components/dialog"
import { Input } from "@workspace/ui/components/input"
import { Label } from "@workspace/ui/components/label"
import { Textarea } from "@workspace/ui/components/textarea"
import { toast } from "sonner"
import { apiFetch } from "@/shared/api/fetcher"

interface ProductCreateDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

interface CreateProductPayload {
  name: string
  sku?: string
  category_id?: string
  description?: string
  image_url?: string
  cost_price?: string
  cost_currency: string
  selling_price?: string
  selling_currency: string
}

async function createProduct(payload: CreateProductPayload) {
  const res = await apiFetch("/api/v1/products", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail?.message ?? "创建失败")
  }
  return res.json()
}

export function ProductCreateDialog({
  open,
  onOpenChange,
}: ProductCreateDialogProps) {
  const queryClient = useQueryClient()

  const [name, setName] = useState("")
  const [sku, setSku] = useState("")
  const [description, setDescription] = useState("")
  const [costPrice, setCostPrice] = useState("")
  const [sellingPrice, setSellingPrice] = useState("")

  const mutation = useMutation({
    mutationFn: createProduct,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["products"] })
      toast.success("产品已创建")
      resetForm()
      onOpenChange(false)
    },
    onError: (err) => {
      toast.error(err.message)
    },
  })

  const resetForm = () => {
    setName("")
    setSku("")
    setDescription("")
    setCostPrice("")
    setSellingPrice("")
  }

  const handleSubmit = () => {
    if (!name.trim()) {
      toast.error("请输入产品名称")
      return
    }
    mutation.mutate({
      name: name.trim(),
      sku: sku.trim() || undefined,
      description: description.trim() || undefined,
      cost_price: costPrice || undefined,
      cost_currency: "CNY",
      selling_price: sellingPrice || undefined,
      selling_currency: "USD",
    })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[480px]">
        <DialogHeader>
          <DialogTitle>新建产品</DialogTitle>
          <DialogDescription>添加新产品到产品库</DialogDescription>
        </DialogHeader>

        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label>产品名称</Label>
            <Input
              placeholder="产品名称"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>

          <div className="grid gap-2">
            <Label>SKU</Label>
            <Input
              placeholder="SKU 编码"
              value={sku}
              onChange={(e) => setSku(e.target.value)}
            />
          </div>

          <div className="grid gap-2">
            <Label>分类</Label>
            <Input placeholder="选择分类..." disabled />
          </div>

          <div className="grid gap-2">
            <Label>描述</Label>
            <Textarea
              placeholder="产品描述..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="grid gap-2">
              <Label>成本价</Label>
              <Input
                type="number"
                placeholder="成本价 (CNY)"
                value={costPrice}
                onChange={(e) => setCostPrice(e.target.value)}
                step="0.01"
                min="0"
              />
            </div>
            <div className="grid gap-2">
              <Label>售价</Label>
              <Input
                type="number"
                placeholder="售价 (USD)"
                value={sellingPrice}
                onChange={(e) => setSellingPrice(e.target.value)}
                step="0.01"
                min="0"
              />
            </div>
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            取消
          </Button>
          <Button onClick={handleSubmit} disabled={mutation.isPending}>
            {mutation.isPending ? "保存中..." : "保存"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
