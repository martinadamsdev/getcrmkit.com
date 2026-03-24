import { useState, useCallback } from "react"
import { useQuery, useMutation } from "@tanstack/react-query"
import { Upload, CheckCircle2, XCircle, AlertTriangle } from "lucide-react"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@workspace/ui/components/dialog"
import { Button } from "@workspace/ui/components/button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@workspace/ui/components/select"
import { Progress } from "@workspace/ui/components/progress"
import { FileUpload } from "@/shared/components/form/file-upload"
import { apiFetch } from "@/shared/api/fetcher"

type SystemField = {
  key: string
  label: string
  required?: boolean
}

type FieldMapping = Record<string, string>

type DataJobStatus = {
  id: string
  status: "pending" | "processing" | "completed" | "failed"
  total_rows: number
  processed_rows: number
  success_count: number
  error_count: number
  errors: { row: number; reason: string }[]
}

type ImportDialogProps = {
  open: boolean
  onOpenChange: (open: boolean) => void
  entityType: "customer" | "product"
  uploadEndpoint: string
  systemFields: SystemField[]
  onComplete: () => void
}

type Step = "upload" | "mapping" | "progress"

async function parseHeaders(file: File): Promise<string[]> {
  const formData = new FormData()
  formData.append("file", file)

  const res = await apiFetch("/api/v1/files/parse-headers", {
    method: "POST",
    body: formData,
  })

  if (!res.ok) throw new Error("Failed to parse file headers")
  const data = await res.json()
  return data.headers
}

async function startImport(
  endpoint: string,
  file: File,
  mapping: FieldMapping,
): Promise<{ job_id: string }> {
  const formData = new FormData()
  formData.append("file", file)
  formData.append("mapping", JSON.stringify(mapping))

  const res = await apiFetch(endpoint, {
    method: "POST",
    body: formData,
  })

  if (!res.ok) throw new Error("Failed to start import")
  return res.json()
}

async function fetchJobStatus(jobId: string): Promise<DataJobStatus> {
  const res = await apiFetch(`/api/v1/data-jobs/${jobId}`)
  if (!res.ok) throw new Error("Failed to fetch job status")
  return res.json()
}

function autoMatchField(
  header: string,
  systemFields: SystemField[],
): string | undefined {
  const normalized = header.toLowerCase().trim()
  // Exact key match
  const exactKey = systemFields.find((f) => f.key === normalized)
  if (exactKey) return exactKey.key
  // Exact label match
  const exactLabel = systemFields.find(
    (f) => f.label.toLowerCase() === normalized,
  )
  if (exactLabel) return exactLabel.key
  // Partial match
  const partial = systemFields.find(
    (f) =>
      normalized.includes(f.key) ||
      f.key.includes(normalized) ||
      normalized.includes(f.label.toLowerCase()) ||
      f.label.toLowerCase().includes(normalized),
  )
  return partial?.key
}

export function ImportDialog({
  open,
  onOpenChange,
  entityType,
  uploadEndpoint,
  systemFields,
  onComplete,
}: ImportDialogProps) {
  const [step, setStep] = useState<Step>("upload")
  const [file, setFile] = useState<File | null>(null)
  const [excelHeaders, setExcelHeaders] = useState<string[]>([])
  const [mapping, setMapping] = useState<FieldMapping>({})
  const [jobId, setJobId] = useState<string | null>(null)

  const entityLabel = entityType === "customer" ? "客户" : "产品"

  // Parse file headers when moving to mapping step
  const parseHeadersMutation = useMutation({
    mutationFn: (f: File) => parseHeaders(f),
    onSuccess: (headers) => {
      setExcelHeaders(headers)
      // Auto-match fields
      const autoMapping: FieldMapping = {}
      for (const header of headers) {
        const match = autoMatchField(header, systemFields)
        if (match) {
          autoMapping[header] = match
        }
      }
      setMapping(autoMapping)
      setStep("mapping")
    },
  })

  // Start import job
  const importMutation = useMutation({
    mutationFn: () => startImport(uploadEndpoint, file!, mapping),
    onSuccess: (data) => {
      setJobId(data.job_id)
      setStep("progress")
    },
  })

  // Poll job status
  const jobQuery = useQuery({
    queryKey: ["data-jobs", jobId],
    queryFn: () => fetchJobStatus(jobId!),
    enabled: !!jobId && step === "progress",
    refetchInterval: (query) => {
      const status = query.state.data?.status
      if (status === "completed" || status === "failed") return false
      return 3000
    },
  })

  const handleFileUpload = useCallback((f: File) => {
    setFile(f)
  }, [])

  const handleNextToMapping = () => {
    if (!file) return
    parseHeadersMutation.mutate(file)
  }

  const handleStartImport = () => {
    importMutation.mutate()
  }

  const handleMappingChange = (header: string, fieldKey: string) => {
    setMapping((prev) => ({
      ...prev,
      [header]: fieldKey === "__none__" ? "" : fieldKey,
    }))
  }

  const handleClose = () => {
    if (jobQuery.data?.status === "completed") {
      onComplete()
    }
    // Reset state
    setStep("upload")
    setFile(null)
    setExcelHeaders([])
    setMapping({})
    setJobId(null)
    onOpenChange(false)
  }

  const progressPercent = jobQuery.data
    ? jobQuery.data.total_rows > 0
      ? Math.round(
          (jobQuery.data.processed_rows / jobQuery.data.total_rows) * 100,
        )
      : 0
    : 0

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>导入{entityLabel}</DialogTitle>
          <DialogDescription>
            {step === "upload" && `上传 Excel 或 CSV 文件以批量导入${entityLabel}`}
            {step === "mapping" && "将文件列映射到系统字段"}
            {step === "progress" && "导入进行中..."}
          </DialogDescription>
        </DialogHeader>

        {/* Step indicators */}
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <span className={step === "upload" ? "font-medium text-foreground" : ""}>
            1. 上传文件
          </span>
          <span>-</span>
          <span className={step === "mapping" ? "font-medium text-foreground" : ""}>
            2. 字段映射
          </span>
          <span>-</span>
          <span className={step === "progress" ? "font-medium text-foreground" : ""}>
            3. 导入结果
          </span>
        </div>

        {/* Step 1: Upload */}
        {step === "upload" && (
          <div className="space-y-4">
            <FileUpload
              accept={{
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
                "application/vnd.ms-excel": [".xls"],
                "text/csv": [".csv"],
              }}
              maxSize={10 * 1024 * 1024}
              onUpload={handleFileUpload}
            />
            {!file && (
              <p className="text-center text-xs text-muted-foreground">
                支持 .xlsx、.xls、.csv 格式，最大 10MB
              </p>
            )}
            <div className="flex justify-end">
              <Button
                onClick={handleNextToMapping}
                disabled={!file || parseHeadersMutation.isPending}
              >
                {parseHeadersMutation.isPending ? "解析中..." : "下一步"}
              </Button>
            </div>
          </div>
        )}

        {/* Step 2: Field Mapping */}
        {step === "mapping" && (
          <div className="space-y-4">
            <p className="text-sm font-medium">字段映射</p>
            <div className="max-h-64 space-y-3 overflow-y-auto">
              {excelHeaders.map((header) => (
                <div
                  key={header}
                  className="flex items-center gap-3"
                >
                  <span className="w-1/3 truncate text-sm" title={header}>
                    {header}
                  </span>
                  <span className="text-muted-foreground">→</span>
                  <Select
                    value={mapping[header] || "__none__"}
                    onValueChange={(value) => handleMappingChange(header, value)}
                  >
                    <SelectTrigger className="w-1/2">
                      <SelectValue placeholder="选择字段" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="__none__">-- 跳过 --</SelectItem>
                      {systemFields.map((field) => (
                        <SelectItem key={field.key} value={field.key}>
                          {field.label}
                          {field.required ? " *" : ""}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              ))}
            </div>
            <RequiredFieldsHint
              systemFields={systemFields}
              mapping={mapping}
            />
            <div className="flex justify-between">
              <Button variant="outline" onClick={() => setStep("upload")}>
                上一步
              </Button>
              <Button
                onClick={handleStartImport}
                disabled={importMutation.isPending}
              >
                {importMutation.isPending ? "提交中..." : "开始导入"}
              </Button>
            </div>
          </div>
        )}

        {/* Step 3: Progress */}
        {step === "progress" && (
          <div className="space-y-4">
            {jobQuery.data?.status === "processing" && (
              <>
                <div className="flex items-center gap-2">
                  <Upload className="size-5 animate-pulse text-primary" />
                  <span className="text-sm">
                    正在导入... {jobQuery.data.processed_rows}/{jobQuery.data.total_rows}
                  </span>
                </div>
                <Progress value={progressPercent} />
              </>
            )}

            {jobQuery.data?.status === "pending" && (
              <>
                <div className="flex items-center gap-2">
                  <Upload className="size-5 animate-pulse text-primary" />
                  <span className="text-sm">正在导入... 准备中</span>
                </div>
                <Progress value={0} />
              </>
            )}

            {jobQuery.data?.status === "completed" && (
              <>
                <div className="flex items-center gap-2 text-green-600">
                  <CheckCircle2 className="size-5" />
                  <span className="text-sm font-medium">
                    导入完成！成功 {jobQuery.data.success_count} 条
                  </span>
                </div>
                {jobQuery.data.error_count > 0 && (
                  <div className="flex items-center gap-2 text-amber-600">
                    <AlertTriangle className="size-4" />
                    <span className="text-xs">
                      {jobQuery.data.error_count} 条记录跳过
                    </span>
                  </div>
                )}
                <div className="flex justify-end">
                  <Button onClick={handleClose}>关闭</Button>
                </div>
              </>
            )}

            {jobQuery.data?.status === "failed" && (
              <>
                <div className="flex items-center gap-2 text-destructive">
                  <XCircle className="size-5" />
                  <span className="text-sm font-medium">导入失败</span>
                </div>
                {jobQuery.data.errors.length > 0 && (
                  <div className="max-h-40 overflow-y-auto rounded border p-3">
                    <p className="mb-2 text-xs font-medium text-muted-foreground">
                      错误详情：
                    </p>
                    <ul className="space-y-1">
                      {jobQuery.data.errors.map((err, i) => (
                        <li
                          key={`${err.row}-${i}`}
                          className="text-xs text-destructive"
                        >
                          第 {err.row} 行：{err.reason}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                <div className="flex justify-end gap-2">
                  <Button variant="outline" onClick={() => { setStep("upload"); setJobId(null); setFile(null) }}>
                    重新上传
                  </Button>
                  <Button onClick={handleClose}>关闭</Button>
                </div>
              </>
            )}

            {/* Loading state before first poll returns */}
            {!jobQuery.data && jobQuery.isLoading && (
              <>
                <div className="flex items-center gap-2">
                  <Upload className="size-5 animate-pulse text-primary" />
                  <span className="text-sm">正在导入... 准备中</span>
                </div>
                <Progress value={0} />
              </>
            )}
          </div>
        )}
      </DialogContent>
    </Dialog>
  )
}

function RequiredFieldsHint({
  systemFields,
  mapping,
}: {
  systemFields: SystemField[]
  mapping: FieldMapping
}) {
  const mappedKeys = new Set(Object.values(mapping).filter(Boolean))
  const missingRequired = systemFields.filter(
    (f) => f.required && !mappedKeys.has(f.key),
  )

  if (missingRequired.length === 0) return null

  return (
    <p className="text-xs text-amber-600">
      <AlertTriangle className="mr-1 inline size-3" />
      必填字段未映射：{missingRequired.map((f) => f.label).join("、")}
    </p>
  )
}
