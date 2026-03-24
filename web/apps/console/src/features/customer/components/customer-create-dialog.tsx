import { useCallback, useEffect, useState } from "react"
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@workspace/ui/components/dialog"
import { Button } from "@workspace/ui/components/button"
import { Input } from "@workspace/ui/components/input"
import { Label } from "@workspace/ui/components/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@workspace/ui/components/select"
import { useDebounce } from "@/shared/hooks/use-debounce"
import { DuplicateWarningDialog } from "./duplicate-warning-dialog"
import type { DuplicateMatch } from "../types"

const SOURCE_OPTIONS = [
  { label: "Alibaba", value: "alibaba" },
  { label: "展会", value: "exhibition" },
  { label: "推荐", value: "referral" },
  { label: "网站", value: "website" },
  { label: "LinkedIn", value: "linkedin" },
  { label: "其他", value: "other" },
]

type CustomerCreateDialogProps = {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSubmit: (data: CustomerFormData) => void
  onCheckDuplicate: (name: string) => Promise<DuplicateMatch[]>
  onViewExisting?: (customerId: string) => void
  isSubmitting?: boolean
}

export type CustomerFormData = {
  name: string
  country?: string
  industry?: string
  source?: string
  website?: string
  company_size?: string
}

export function CustomerCreateDialog({
  open,
  onOpenChange,
  onSubmit,
  onCheckDuplicate,
  onViewExisting,
  isSubmitting = false,
}: CustomerCreateDialogProps) {
  const [name, setName] = useState("")
  const [country, setCountry] = useState("")
  const [industry, setIndustry] = useState("")
  const [source, setSource] = useState("")
  const [website, setWebsite] = useState("")
  const [companySize, setCompanySize] = useState("")
  const [duplicates, setDuplicates] = useState<DuplicateMatch[]>([])
  const [showDuplicateWarning, setShowDuplicateWarning] = useState(false)
  const [duplicateChecked, setDuplicateChecked] = useState(false)

  const debouncedName = useDebounce(name, 500)

  const checkDuplicate = useCallback(async () => {
    if (!debouncedName.trim()) {
      setDuplicates([])
      return
    }
    try {
      const result = await onCheckDuplicate(debouncedName)
      setDuplicates(result)
      setDuplicateChecked(true)
      if (result.length > 0) {
        setShowDuplicateWarning(true)
      }
    } catch {
      // Silently handle check errors
    }
  }, [debouncedName, onCheckDuplicate])

  useEffect(() => {
    if (debouncedName.trim()) {
      checkDuplicate()
    }
  }, [debouncedName, checkDuplicate])

  const resetForm = () => {
    setName("")
    setCountry("")
    setIndustry("")
    setSource("")
    setWebsite("")
    setCompanySize("")
    setDuplicates([])
    setShowDuplicateWarning(false)
    setDuplicateChecked(false)
  }

  const handleOpenChange = (isOpen: boolean) => {
    if (!isOpen) resetForm()
    onOpenChange(isOpen)
  }

  const handleSubmit = () => {
    if (!name.trim()) return
    onSubmit({
      name: name.trim(),
      country: country || undefined,
      industry: industry || undefined,
      source: source || undefined,
      website: website || undefined,
      company_size: companySize || undefined,
    })
  }

  const handleIgnoreDuplicate = () => {
    setShowDuplicateWarning(false)
    handleSubmit()
  }

  const isSubmitDisabled = !name.trim() || isSubmitting

  return (
    <>
      <Dialog open={open} onOpenChange={handleOpenChange}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>新建客户</DialogTitle>
          </DialogHeader>
          <div className="flex flex-col gap-4 py-4">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="customer-name">
                公司名 <span className="text-destructive">*</span>
              </Label>
              <Input
                id="customer-name"
                value={name}
                onChange={(e) => {
                  setName(e.target.value)
                  setDuplicateChecked(false)
                }}
                placeholder="输入公司名称"
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <Label htmlFor="customer-country">国家</Label>
              <Select value={country} onValueChange={setCountry}>
                <SelectTrigger id="customer-country">
                  <SelectValue placeholder="选择国家" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="CN">中国</SelectItem>
                  <SelectItem value="US">美国</SelectItem>
                  <SelectItem value="GB">英国</SelectItem>
                  <SelectItem value="DE">德国</SelectItem>
                  <SelectItem value="JP">日本</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="flex flex-col gap-1.5">
              <Label htmlFor="customer-industry">行业</Label>
              <Select value={industry} onValueChange={setIndustry}>
                <SelectTrigger id="customer-industry">
                  <SelectValue placeholder="选择行业" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="electronics">电子</SelectItem>
                  <SelectItem value="textiles">纺织</SelectItem>
                  <SelectItem value="machinery">机械</SelectItem>
                  <SelectItem value="chemicals">化工</SelectItem>
                  <SelectItem value="furniture">家具</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="flex flex-col gap-1.5">
              <Label htmlFor="customer-source">来源</Label>
              <Select value={source} onValueChange={setSource}>
                <SelectTrigger id="customer-source">
                  <SelectValue placeholder="选择来源" />
                </SelectTrigger>
                <SelectContent>
                  {SOURCE_OPTIONS.map((opt) => (
                    <SelectItem key={opt.value} value={opt.value}>
                      {opt.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="flex flex-col gap-1.5">
              <Label htmlFor="customer-website">网站</Label>
              <Input
                id="customer-website"
                value={website}
                onChange={(e) => setWebsite(e.target.value)}
                placeholder="https://example.com"
              />
            </div>
          </div>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => handleOpenChange(false)}
            >
              取消
            </Button>
            <Button
              onClick={handleSubmit}
              disabled={isSubmitDisabled}
            >
              {isSubmitting ? "创建中..." : "创建"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <DuplicateWarningDialog
        open={showDuplicateWarning}
        onOpenChange={setShowDuplicateWarning}
        duplicates={duplicates}
        onIgnore={handleIgnoreDuplicate}
        onViewExisting={(id) => {
          setShowDuplicateWarning(false)
          handleOpenChange(false)
          onViewExisting?.(id)
        }}
      />
    </>
  )
}
