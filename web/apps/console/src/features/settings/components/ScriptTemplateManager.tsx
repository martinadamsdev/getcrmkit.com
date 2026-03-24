import { useState } from "react"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { Button } from "@workspace/ui/components/button"
import { Card, CardContent, CardHeader, CardTitle } from "@workspace/ui/components/card"
import { Badge } from "@workspace/ui/components/badge"
import { Label } from "@workspace/ui/components/label"
import { Textarea } from "@workspace/ui/components/textarea"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@workspace/ui/components/dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@workspace/ui/components/select"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@workspace/ui/components/alert-dialog"
import { Plus, Pencil, Trash2 } from "lucide-react"
import { toast } from "sonner"

import { SCRIPT_SCENES } from "@/shared/lib/constants"
import { apiFetch } from "@/shared/api/fetcher"

interface ScriptTemplate {
  id: string
  scene: string
  content: string
  is_system: boolean
}

function getSceneLabel(scene: string): string {
  return SCRIPT_SCENES.find((s) => s.value === scene)?.label ?? scene
}

export function ScriptTemplateManager() {
  const queryClient = useQueryClient()
  const [createOpen, setCreateOpen] = useState(false)
  const [scene, setScene] = useState(SCRIPT_SCENES[0].value)
  const [content, setContent] = useState("")

  const { data } = useQuery<{ items: ScriptTemplate[]; total: number }>({
    queryKey: ["script-templates"],
    queryFn: async () => {
      const res = await apiFetch("/api/v1/script-templates")
      if (!res.ok) throw new Error("Failed to fetch templates")
      return res.json()
    },
  })

  const deleteMutation = useMutation({
    mutationFn: async (id: string) => {
      await apiFetch(`/api/v1/script-templates/${id}`, { method: "DELETE" })
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["script-templates"] })
      toast.success("模板已删除")
    },
  })

  const templates = data?.items ?? []
  const systemTemplates = templates.filter((t) => t.is_system)
  const userTemplates = templates.filter((t) => !t.is_system)

  function handleCreate() {
    // TODO: Wire to POST /api/v1/script-templates
    toast.info("模板创建功能开发中")
    setCreateOpen(false)
    setScene(SCRIPT_SCENES[0].value)
    setContent("")
  }

  return (
    <div className="max-w-3xl space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">话术模板</h2>
        <Button onClick={() => setCreateOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          新建模板
        </Button>
      </div>

      {/* System templates */}
      <div>
        <h3 className="mb-3 text-lg font-medium">系统模板</h3>
        {systemTemplates.length === 0 ? (
          <p className="text-sm text-muted-foreground">暂无系统模板</p>
        ) : (
          <div className="space-y-3">
            {systemTemplates.map((tpl) => (
              <Card key={tpl.id}>
                <CardContent className="flex items-start gap-3 py-4">
                  <Badge variant="secondary">{getSceneLabel(tpl.scene)}</Badge>
                  <p className="flex-1 text-sm">{tpl.content}</p>
                  <span className="text-xs text-muted-foreground">系统模板不可编辑</span>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* User templates */}
      <div>
        <h3 className="mb-3 text-lg font-medium">我的模板</h3>
        {userTemplates.length === 0 ? (
          <p className="text-sm text-muted-foreground">暂无自定义模板</p>
        ) : (
          <div className="space-y-3">
            {userTemplates.map((tpl) => (
              <Card key={tpl.id}>
                <CardContent className="flex items-start gap-3 py-4">
                  <Badge variant="outline">{getSceneLabel(tpl.scene)}</Badge>
                  <p className="flex-1 text-sm">{tpl.content}</p>
                  <div className="flex gap-1">
                    <Button variant="ghost" size="icon" aria-label="编辑">
                      <Pencil className="h-4 w-4" />
                    </Button>
                    <AlertDialog>
                      <AlertDialogTrigger asChild>
                        <Button variant="ghost" size="icon" aria-label="删除">
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </AlertDialogTrigger>
                      <AlertDialogContent>
                        <AlertDialogHeader>
                          <AlertDialogTitle>确认删除</AlertDialogTitle>
                          <AlertDialogDescription>
                            确定要删除这个模板吗？此操作不可撤销。
                          </AlertDialogDescription>
                        </AlertDialogHeader>
                        <AlertDialogFooter>
                          <AlertDialogCancel>取消</AlertDialogCancel>
                          <AlertDialogAction onClick={() => deleteMutation.mutate(tpl.id)}>
                            确认删除
                          </AlertDialogAction>
                        </AlertDialogFooter>
                      </AlertDialogContent>
                    </AlertDialog>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Create dialog */}
      <Dialog open={createOpen} onOpenChange={setCreateOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>新建话术模板</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label>场景</Label>
              <Select value={scene} onValueChange={setScene}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {SCRIPT_SCENES.map((s) => (
                    <SelectItem key={s.value} value={s.value}>
                      {s.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>内容</Label>
              <Textarea
                rows={6}
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="输入话术模板内容..."
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setCreateOpen(false)}>
              取消
            </Button>
            <Button onClick={handleCreate} disabled={!content.trim()}>
              保存
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
