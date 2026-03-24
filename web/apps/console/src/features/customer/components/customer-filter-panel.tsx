import { Button } from "@workspace/ui/components/button"
import { Label } from "@workspace/ui/components/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@workspace/ui/components/select"
import { GradeBadge } from "@/shared/components/business/grade-badge"
import { ToggleGroup, ToggleGroupItem } from "@workspace/ui/components/toggle-group"
import type { CustomerFilters } from "../types"

const SOURCE_OPTIONS = [
  { label: "Alibaba", value: "alibaba" },
  { label: "展会", value: "exhibition" },
  { label: "推荐", value: "referral" },
  { label: "网站", value: "website" },
  { label: "LinkedIn", value: "linkedin" },
  { label: "其他", value: "other" },
]

const FOLLOW_STATUS_OPTIONS = [
  { label: "新建", value: "new" },
  { label: "已联系", value: "contacted" },
  { label: "已报价", value: "quoted" },
  { label: "已寄样", value: "sample_sent" },
  { label: "谈判中", value: "negotiating" },
  { label: "已下单", value: "ordered" },
  { label: "已流失", value: "lost" },
]

const GRADE_OPTIONS = [
  { name: "A", color: "#22c55e" },
  { name: "B", color: "#3b82f6" },
  { name: "C", color: "#f59e0b" },
  { name: "D", color: "#9ca3af" },
]

type CustomerFilterPanelProps = {
  filters: CustomerFilters
  onChange: (key: string, value: string | null) => void
  onReset: () => void
  className?: string
}

export function CustomerFilterPanel({
  filters,
  onChange,
  onReset,
  className,
}: CustomerFilterPanelProps) {
  const hasActiveFilters = Object.values(filters).some(
    (v) => v !== null && v !== undefined,
  )

  return (
    <div
      className={`flex flex-col gap-4 rounded-lg border p-4 ${className ?? ""}`}
    >
      {/* Grade filter */}
      <div className="flex flex-col gap-1.5">
        <Label>等级</Label>
        <ToggleGroup
          type="single"
          value={filters.grade_id ?? ""}
          onValueChange={(v) => onChange("grade_id", v || null)}
        >
          {GRADE_OPTIONS.map((g) => (
            <ToggleGroupItem key={g.name} value={g.name} aria-label={`Grade ${g.name}`}>
              <GradeBadge grade={g.name} color={g.color} />
            </ToggleGroupItem>
          ))}
        </ToggleGroup>
      </div>

      {/* Source filter */}
      <div className="flex flex-col gap-1.5">
        <Label>来源</Label>
        <Select
          value={filters.source ?? ""}
          onValueChange={(v) => onChange("source", v || null)}
        >
          <SelectTrigger>
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

      {/* Country filter */}
      <div className="flex flex-col gap-1.5">
        <Label>国家</Label>
        <Select
          value={filters.country ?? ""}
          onValueChange={(v) => onChange("country", v || null)}
        >
          <SelectTrigger>
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

      {/* Industry filter */}
      <div className="flex flex-col gap-1.5">
        <Label>行业</Label>
        <Select
          value={filters.industry ?? ""}
          onValueChange={(v) => onChange("industry", v || null)}
        >
          <SelectTrigger>
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

      {/* Follow status filter */}
      <div className="flex flex-col gap-1.5">
        <Label>跟进状态</Label>
        <Select
          value={filters.follow_status ?? ""}
          onValueChange={(v) => onChange("follow_status", v || null)}
        >
          <SelectTrigger>
            <SelectValue placeholder="选择状态" />
          </SelectTrigger>
          <SelectContent>
            {FOLLOW_STATUS_OPTIONS.map((opt) => (
              <SelectItem key={opt.value} value={opt.value}>
                {opt.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Clear all */}
      {hasActiveFilters && (
        <Button
          variant="ghost"
          size="sm"
          onClick={onReset}
          aria-label="Clear all filters"
        >
          清除全部筛选
        </Button>
      )}
    </div>
  )
}
