import { Download, Plus, Upload } from "lucide-react"
import { Button } from "@workspace/ui/components/button"
import { SearchInput } from "@/shared/components/form/search-input"

interface ProductToolbarProps {
  onSearch: (query: string) => void
  onCreateClick: () => void
  onImportClick: () => void
  onExportClick: () => void
}

export function ProductToolbar({
  onSearch,
  onCreateClick,
  onImportClick,
  onExportClick,
}: ProductToolbarProps) {
  return (
    <div className="flex items-center justify-between gap-4 px-4 py-3">
      <SearchInput
        placeholder="搜索产品..."
        onSearch={onSearch}
        debounceMs={300}
        className="flex-1 max-w-sm"
      />
      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={onImportClick}
          aria-label="导入"
        >
          <Upload className="mr-1.5 h-3.5 w-3.5" />
          导入
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={onExportClick}
          aria-label="导出"
        >
          <Download className="mr-1.5 h-3.5 w-3.5" />
          导出
        </Button>
        <Button onClick={onCreateClick}>
          <Plus className="mr-1.5 h-4 w-4" />
          新建产品
        </Button>
      </div>
    </div>
  )
}
