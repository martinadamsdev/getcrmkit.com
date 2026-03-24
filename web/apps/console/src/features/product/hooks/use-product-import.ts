import { useState } from "react"
import { useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import { apiFetch } from "@/shared/api/fetcher"

interface ImportState {
  uploading: boolean
  jobId: string | null
  status: "idle" | "uploading" | "processing" | "completed" | "failed"
}

export function useProductImport() {
  const queryClient = useQueryClient()
  const [state, setState] = useState<ImportState>({
    uploading: false,
    jobId: null,
    status: "idle",
  })

  const importFile = async (file: File) => {
    setState({ uploading: true, jobId: null, status: "uploading" })
    try {
      const formData = new FormData()
      formData.append("file", file)

      const res = await apiFetch("/api/v1/products/import", {
        method: "POST",
        body: formData,
      })

      if (!res.ok) throw new Error("Upload failed")
      const data = await res.json()

      setState({ uploading: false, jobId: data.job_id, status: "processing" })
      toast.success("文件已上传，正在处理...")

      pollJobStatus(data.job_id)
    } catch {
      setState({ uploading: false, jobId: null, status: "failed" })
      toast.error("导入失败，请重试")
    }
  }

  const pollJobStatus = async (jobId: string) => {
    const maxAttempts = 30
    for (let i = 0; i < maxAttempts; i++) {
      await new Promise((r) => setTimeout(r, 2000))
      try {
        const res = await apiFetch(`/api/v1/data-jobs/${jobId}`)
        if (!res.ok) continue
        const job = await res.json()

        if (job.status === "completed") {
          setState((prev) => ({ ...prev, status: "completed" }))
          queryClient.invalidateQueries({ queryKey: ["products"] })
          toast.success(`导入完成: ${job.processed_count} 条记录`)
          return
        }
        if (job.status === "failed") {
          setState((prev) => ({ ...prev, status: "failed" }))
          toast.error(`导入失败: ${job.error_message}`)
          return
        }
      } catch {
        // Continue polling
      }
    }
    toast.error("导入超时，请检查任务状态")
  }

  return { ...state, importFile }
}
