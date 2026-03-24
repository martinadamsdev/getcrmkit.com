import { useState, useCallback, useEffect } from "react"
import { useNavigate } from "@tanstack/react-router"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import { Button } from "@workspace/ui/components/button"
import { Card, CardContent } from "@workspace/ui/components/card"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@workspace/ui/components/select"
import { Input } from "@workspace/ui/components/input"
import { Label } from "@workspace/ui/components/label"
import { Loader2, Save } from "lucide-react"
import { CustomerPicker } from "@/shared/components/business/customer-picker"
import { QuotationHeader } from "./quotation-header"
import { QuotationItemTable } from "./quotation-item-table"
import { ProfitPanel } from "./profit-panel"
import { StatusActions } from "./status-actions"
import { ExportDropdown } from "./export-dropdown"
import { useQuotationProfitCalc } from "../hooks/use-quotation-profit-calc"
import { useQuotationEditorStore } from "../stores/quotation-editor.store"
import { TRADE_TERMS, CURRENCIES, type QuotationStatus } from "@/shared/lib/constants"
import { apiFetch } from "@/shared/api/fetcher"

type QuotationEditorProps = {
  quotationId?: string
  initialData?: any
  onConvertToOrder?: (quotationId: string) => void
  isConverting?: boolean
}

export function QuotationEditor({
  quotationId,
  initialData,
  onConvertToOrder,
  isConverting,
}: QuotationEditorProps) {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const store = useQuotationEditorStore()

  const [quotationNo, setQuotationNo] = useState(
    initialData?.quotation_no ?? "",
  )
  const [customerId, setCustomerId] = useState<string | undefined>(
    initialData?.customer_id ?? undefined,
  )
  const [customerName, setCustomerName] = useState(
    initialData?.customer_name ?? "",
  )
  const [status, setStatus] = useState<QuotationStatus>(
    initialData?.status ?? "draft",
  )
  const [exportLang, setExportLang] = useState<"en" | "zh">("en")
  const [notes, setNotes] = useState(initialData?.notes ?? "")

  const isNew = !quotationId

  useEffect(() => {
    if (initialData) {
      store.loadQuotation({
        items: (initialData.items ?? []).map((i: any) => ({
          id: i.id,
          productId: i.product_id,
          productName: i.product_name,
          material: i.material,
          quantity: i.quantity,
          costPrice: Number(i.cost_price),
          costCurrency: i.cost_currency ?? "CNY",
          unitPrice: Number(i.unit_price),
          sellingCurrency: i.selling_currency ?? "USD",
          multiplier: i.multiplier,
          subtotal: Number(i.subtotal),
          customizationIds: i.customization_ids ?? [],
          customizationCost: Number(i.customization_cost ?? 0),
          notes: i.notes ?? "",
          position: i.sort_order ?? 0,
        })),
        tradeTerm: initialData.trade_term ?? "FOB",
        currency: initialData.currency ?? "USD",
        freight: Number(initialData.freight ?? 0),
        insurance: Number(initialData.insurance ?? 0),
        otherCost: Number(initialData.other_cost ?? 0),
        exchangeRate: Number(initialData.exchange_rate ?? 1.0),
      })
    }
    return () => {
      store.reset()
    }
  }, [initialData])

  useQuotationProfitCalc(quotationId ?? null)

  const saveMutation = useMutation({
    mutationFn: async () => {
      const payload = {
        quotation_no: quotationNo,
        customer_id: customerId,
        trade_term: store.tradeTerm,
        currency: store.currency,
        exchange_rate: store.exchangeRate,
        freight: store.freight,
        insurance: store.insurance,
        other_cost: store.otherCost,
        notes,
        items: store.items.map((i) => ({
          product_id: i.productId,
          product_name: i.productName,
          material: i.material,
          quantity: i.quantity,
          cost_price: i.costPrice,
          cost_currency: i.costCurrency,
          unit_price: i.unitPrice,
          selling_currency: i.sellingCurrency,
          subtotal: i.subtotal,
          customization_ids: i.customizationIds,
          customization_cost: i.customizationCost,
          notes: i.notes,
          sort_order: i.position,
        })),
      }

      const url = isNew
        ? "/api/v1/quotations"
        : `/api/v1/quotations/${quotationId}`
      const method = isNew ? "POST" : "PUT"

      const res = await apiFetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })

      if (!res.ok) throw new Error("Save failed")
      return res.json()
    },
    onSuccess: (data) => {
      toast.success(isNew ? "报价单已创建" : "报价单已保存")
      queryClient.invalidateQueries({ queryKey: ["quotations"] })
      queryClient.invalidateQueries({ queryKey: ["nav-badges"] })
      if (isNew && data.id) {
        navigate({ to: "/quotations/$id", params: { id: data.id } })
      }
    },
    onError: () => {
      toast.error("保存失败，请重试")
    },
  })

  const transitionMutation = useMutation({
    mutationFn: async (targetStatus: QuotationStatus) => {
      const res = await apiFetch(
        `/api/v1/quotations/${quotationId}/status`,
        {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ status: targetStatus }),
        },
      )
      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error(err.detail ?? "Status transition failed")
      }
      return res.json()
    },
    onSuccess: (_, targetStatus) => {
      setStatus(targetStatus)
      toast.success("状态已更新")
      queryClient.invalidateQueries({ queryKey: ["quotations"] })
      queryClient.invalidateQueries({
        queryKey: ["quotation", quotationId],
      })
    },
    onError: (err) => {
      toast.error(err instanceof Error ? err.message : "状态变更失败")
    },
  })

  const handleTransition = useCallback(
    (targetStatus: QuotationStatus) => {
      if (targetStatus === "converted" && quotationId && onConvertToOrder) {
        onConvertToOrder(quotationId)
      } else {
        transitionMutation.mutate(targetStatus)
      }
    },
    [transitionMutation, onConvertToOrder, quotationId],
  )

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_320px]">
      {/* Left: Editor */}
      <div className="space-y-6">
        <QuotationHeader
          quotationNo={quotationNo}
          onQuotationNoChange={setQuotationNo}
          status={status}
          isNew={isNew}
        />

        {/* Customer Section */}
        <Card>
          <CardContent className="pt-6 space-y-4">
            <div>
              <Label>客户</Label>
              <CustomerPicker
                value={customerId}
                displayName={customerName}
                onChange={(id, name) => {
                  setCustomerId(id)
                  setCustomerName(name)
                }}
              />
            </div>
          </CardContent>
        </Card>

        {/* Trade Terms + Currency */}
        <Card>
          <CardContent className="pt-6">
            <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
              <div>
                <Label>贸易条款</Label>
                <Select
                  value={store.tradeTerm}
                  onValueChange={store.setTradeTerm}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {TRADE_TERMS.map((t) => (
                      <SelectItem key={t.value} value={t.value}>
                        {t.value}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>币种</Label>
                <Select
                  value={store.currency}
                  onValueChange={store.setCurrency}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {CURRENCIES.map((c) => (
                      <SelectItem key={c.code} value={c.code}>
                        {c.symbol} {c.code}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>运费 ({store.currency})</Label>
                <Input
                  type="number"
                  value={store.freight}
                  onChange={(e) => store.setFreight(Number(e.target.value))}
                  min={0}
                  step={0.01}
                />
              </div>
              <div>
                <Label>保险 ({store.currency})</Label>
                <Input
                  type="number"
                  value={store.insurance}
                  onChange={(e) =>
                    store.setInsurance(Number(e.target.value))
                  }
                  min={0}
                  step={0.01}
                />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Line Items */}
        <Card>
          <CardContent className="pt-6">
            <QuotationItemTable />
          </CardContent>
        </Card>

        {/* Notes */}
        <Card>
          <CardContent className="pt-6">
            <Label>备注</Label>
            <textarea
              className="mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              rows={3}
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="报价备注..."
            />
          </CardContent>
        </Card>

        {/* Actions */}
        <div className="flex items-center justify-between">
          <div className="flex gap-2">
            <Button
              onClick={() => saveMutation.mutate()}
              disabled={saveMutation.isPending}
            >
              {saveMutation.isPending ? (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                <Save className="mr-2 h-4 w-4" />
              )}
              {isNew ? "创建报价" : "保存"}
            </Button>
            {!isNew && (
              <ExportDropdown
                quotationId={quotationId!}
                lang={exportLang}
                onLangChange={setExportLang}
              />
            )}
          </div>
          {!isNew && (
            <StatusActions
              currentStatus={status}
              onTransition={handleTransition}
              isLoading={transitionMutation.isPending}
            />
          )}
        </div>
      </div>

      {/* Right: Profit Panel */}
      <div className="hidden lg:block">
        <ProfitPanel />
      </div>
    </div>
  )
}
