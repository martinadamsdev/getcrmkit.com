import { useState } from "react"
import { Plus, X } from "lucide-react"
import { Tabs, TabsList, TabsTrigger } from "@workspace/ui/components/tabs"
import { Button } from "@workspace/ui/components/button"
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@workspace/ui/components/dialog"
import { Input } from "@workspace/ui/components/input"
import { Label } from "@workspace/ui/components/label"
import type { SavedView } from "../types"

type SavedViewTabsProps = {
  views: SavedView[]
  activeViewId?: string | null
  onViewChange: (filters: Record<string, string | null>) => void
  onSave: (name: string) => void
  onDelete: (viewId: string) => void
  className?: string
}

export function SavedViewTabs({
  views,
  activeViewId,
  onViewChange,
  onSave,
  onDelete,
  className,
}: SavedViewTabsProps) {
  const [saveDialogOpen, setSaveDialogOpen] = useState(false)
  const [viewName, setViewName] = useState("")

  const handleSave = () => {
    if (viewName.trim()) {
      onSave(viewName.trim())
      setViewName("")
      setSaveDialogOpen(false)
    }
  }

  return (
    <>
      <Tabs
        value={activeViewId ?? "all"}
        onValueChange={(id) => {
          if (id === "all") {
            onViewChange({})
          } else {
            const view = views.find((v) => v.id === id)
            if (view) {
              onViewChange(view.filter_config)
            }
          }
        }}
        className={className}
      >
        <TabsList>
          <TabsTrigger value="all">全部</TabsTrigger>
          {views.map((view) => (
            <TabsTrigger key={view.id} value={view.id} className="group">
              {view.name}
              <button
                type="button"
                aria-label={`Delete view ${view.name}`}
                className="ml-1 hidden rounded-sm opacity-70 hover:opacity-100 group-hover:inline-flex"
                onClick={(e) => {
                  e.stopPropagation()
                  onDelete(view.id)
                }}
              >
                <X className="size-3" />
              </button>
            </TabsTrigger>
          ))}
          <Button
            variant="ghost"
            size="sm"
            className="ml-1 h-7 px-2"
            onClick={() => setSaveDialogOpen(true)}
            aria-label="Save current view"
          >
            <Plus className="size-3.5" />
          </Button>
        </TabsList>
      </Tabs>

      <Dialog open={saveDialogOpen} onOpenChange={setSaveDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>保存当前视图</DialogTitle>
          </DialogHeader>
          <div className="py-4">
            <Label htmlFor="view-name">视图名称</Label>
            <Input
              id="view-name"
              value={viewName}
              onChange={(e) => setViewName(e.target.value)}
              placeholder="输入视图名称"
              onKeyDown={(e) => {
                if (e.key === "Enter") handleSave()
              }}
            />
          </div>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setSaveDialogOpen(false)}
            >
              取消
            </Button>
            <Button onClick={handleSave} disabled={!viewName.trim()}>
              保存
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  )
}
