import { useState, useCallback } from "react"
import { Download, Loader2 } from "lucide-react"
import { Button } from "@workspace/ui/components/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@workspace/ui/components/dropdown-menu"
import {
  ToggleGroup,
  ToggleGroupItem,
} from "@workspace/ui/components/toggle-group"
import { toast } from "sonner"

const EXPORT_TYPES = [
  { type: "quotation", label: "报价单" },
  { type: "quotation_print", label: "打印版" },
  { type: "pi", label: "PI" },
  { type: "packing_list", label: "装箱单" },
  { type: "ci", label: "CI" },
  { type: "all", label: "全部下载" },
] as const

type ExportDropdownProps = {
  quotationId: string
  quotationNo?: string
  lang: "en" | "zh"
  onLangChange: (lang: "en" | "zh") => void
  isExporting?: boolean
}

export function ExportDropdown({
  quotationId,
  quotationNo,
  lang,
  onLangChange,
  isExporting = false,
}: ExportDropdownProps) {
  const [downloading, setDownloading] = useState<string | null>(null)

  const handleExport = useCallback(
    async (type: string) => {
      setDownloading(type)
      try {
        const res = await fetch(
          `/api/v1/quotations/${quotationId}/export?type=${type}&lang=${lang}`,
        )
        if (!res.ok) {
          throw new Error("Export failed")
        }
        const blob = await res.blob()
        const url = URL.createObjectURL(blob)
        const a = document.createElement("a")
        const ext = type === "all" ? "zip" : "xlsx"
        a.href = url
        a.download = `${quotationNo ?? quotationId}_${type}.${ext}`
        a.click()
        URL.revokeObjectURL(url)
        toast.success("导出成功")
      } catch {
        toast.error("导出失败，请重试")
      } finally {
        setDownloading(null)
      }
    },
    [quotationId, lang],
  )

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" disabled={isExporting}>
          {isExporting ? (
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          ) : (
            <Download className="mr-2 h-4 w-4" />
          )}
          导出
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-48">
        <div className="px-2 py-1.5">
          <ToggleGroup
            type="single"
            value={lang}
            onValueChange={(val) => {
              if (val) onLangChange(val as "en" | "zh")
            }}
            className="justify-start"
          >
            <ToggleGroupItem value="en" className="text-xs">
              EN
            </ToggleGroupItem>
            <ToggleGroupItem value="zh" className="text-xs">
              中
            </ToggleGroupItem>
          </ToggleGroup>
        </div>
        <DropdownMenuSeparator />
        {EXPORT_TYPES.map(({ type, label }) => (
          <DropdownMenuItem
            key={type}
            onClick={() => handleExport(type)}
            disabled={downloading !== null}
          >
            {downloading === type && (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            )}
            {label}
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
