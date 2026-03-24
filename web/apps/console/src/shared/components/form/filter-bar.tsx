import { Filter } from "lucide-react"
import { Button } from "@workspace/ui/components/button"
import { Badge } from "@workspace/ui/components/badge"
import { Input } from "@workspace/ui/components/input"
import { Label } from "@workspace/ui/components/label"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@workspace/ui/components/popover"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@workspace/ui/components/select"
import type { FilterDef } from "@/shared/hooks/use-filters"

type FilterBarProps = {
  filters: FilterDef[]
  values: Record<string, string | null>
  onChange: (key: string, value: string | null) => void
  onReset: () => void
  className?: string
}

export function FilterBar({
  filters,
  values,
  onChange,
  onReset,
  className,
}: FilterBarProps) {
  const activeCount = Object.values(values).filter(Boolean).length

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline" className={className} aria-label="Filter">
          <Filter className="mr-2 size-4" />
          Filter
          {activeCount > 0 && (
            <Badge variant="default" className="ml-2">
              {activeCount}
            </Badge>
          )}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-80">
        <div className="flex flex-col gap-3">
          {filters.map((filter) => (
            <div key={filter.key} className="flex flex-col gap-1.5">
              <Label>{filter.label}</Label>
              {filter.type === "select" && filter.options ? (
                <Select
                  value={values[filter.key] ?? ""}
                  onValueChange={(v) => onChange(filter.key, v || null)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder={filter.label} />
                  </SelectTrigger>
                  <SelectContent>
                    {filter.options.map((opt) => (
                      <SelectItem key={opt.value} value={opt.value}>
                        {opt.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              ) : (
                <Input
                  placeholder={filter.label}
                  value={values[filter.key] ?? ""}
                  onChange={(e) =>
                    onChange(filter.key, e.target.value || null)
                  }
                />
              )}
            </div>
          ))}
          {activeCount > 0 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onReset}
              aria-label="Clear all filters"
            >
              Clear all
            </Button>
          )}
        </div>
      </PopoverContent>
    </Popover>
  )
}
