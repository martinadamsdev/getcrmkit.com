import { useState, useCallback } from "react"
import { FileSpreadsheet, Loader2 } from "lucide-react"
import { Button } from "@workspace/ui/components/button"
import { toast } from "sonner"
import { apiFetch } from "@/shared/api/fetcher"

interface GeneratePIButtonProps {
  orderId: string
}

export function GeneratePIButton({ orderId }: GeneratePIButtonProps) {
  const [isGenerating, setIsGenerating] = useState(false)

  const handleGenerate = useCallback(async () => {
    setIsGenerating(true)
    try {
      const res = await apiFetch(`/api/v1/orders/${orderId}/generate-pi`, {
        method: "POST",
      })
      if (!res.ok) throw new Error("PI generation failed")

      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      try {
        const a = document.createElement("a")
        a.href = url
        a.download = `PI-${orderId}.xlsx`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
      } finally {
        setTimeout(() => URL.revokeObjectURL(url), 100)
      }
      toast.success("PI 已生成")
    } catch {
      toast.error("PI 生成失败，请重试")
    } finally {
      setIsGenerating(false)
    }
  }, [orderId])

  return (
    <Button
      variant="outline"
      onClick={handleGenerate}
      disabled={isGenerating}
    >
      {isGenerating ? (
        <>
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          生成中...
        </>
      ) : (
        <>
          <FileSpreadsheet className="mr-2 h-4 w-4" />
          生成 PI
        </>
      )}
    </Button>
  )
}
