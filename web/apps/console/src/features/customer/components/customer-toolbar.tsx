import { Download, Plus, Upload } from "lucide-react"
import { Button } from "@workspace/ui/components/button"
import { SearchInput } from "@/shared/components/form/search-input"

type CustomerToolbarProps = {
  onSearch: (q: string) => void
  onFilterClick: () => void
  activeFilterCount: number
  defaultSearchValue?: string
  onCreateClick: () => void
  onImportClick?: () => void
  onExportClick?: () => void
}

export function CustomerToolbar({
  onSearch,
  defaultSearchValue,
  onCreateClick,
  onImportClick,
  onExportClick,
}: CustomerToolbarProps) {
  return (
    <div className="flex items-center gap-3">
      <SearchInput
        placeholder="搜索客户名/联系人/邮箱..."
        onSearch={onSearch}
        defaultValue={defaultSearchValue}
        className="w-72"
      />
      <div className="flex-1" />
      {onImportClick && (
        <Button variant="outline" size="sm" onClick={onImportClick}>
          <Upload className="mr-2 size-4" />
          导入
        </Button>
      )}
      {onExportClick && (
        <Button variant="outline" size="sm" onClick={onExportClick}>
          <Download className="mr-2 size-4" />
          导出
        </Button>
      )}
      <Button onClick={onCreateClick}>
        <Plus className="mr-2 size-4" />
        新建客户
      </Button>
    </div>
  )
}
