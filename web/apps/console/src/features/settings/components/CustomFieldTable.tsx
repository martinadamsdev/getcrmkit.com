import { Button } from "@workspace/ui/components/button"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@workspace/ui/components/table"
import { Badge } from "@workspace/ui/components/badge"
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
import { Trash2 } from "lucide-react"
import { toast } from "sonner"

const TYPE_LABELS: Record<string, string> = {
  text: "文本",
  number: "数字",
  date: "日期",
  select: "下拉选择",
  boolean: "是/否",
}

interface CustomFieldDefinition {
  id: string
  entity: string
  name: string
  type: string
  required: boolean
  options: string[]
  sort_order: number
}

interface CustomFieldTableProps {
  fields: CustomFieldDefinition[]
  entity: string
}

export function CustomFieldTable({ fields, entity: _entity }: CustomFieldTableProps) {
  function handleDelete(_id: string) {
    // TODO: Wire to DELETE /api/v1/custom-field-definitions/{id}
    toast.info("字段删除功能开发中")
  }

  if (fields.length === 0) {
    return (
      <div className="py-8 text-center text-muted-foreground">
        暂无自定义字段
      </div>
    )
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>名称</TableHead>
          <TableHead>类型</TableHead>
          <TableHead>必填</TableHead>
          <TableHead className="w-[80px]">操作</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {fields.map((field) => (
          <TableRow key={field.id}>
            <TableCell className="font-medium">{field.name}</TableCell>
            <TableCell>
              <Badge variant="secondary">{TYPE_LABELS[field.type] ?? field.type}</Badge>
            </TableCell>
            <TableCell>{field.required ? "是" : "否"}</TableCell>
            <TableCell>
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
                      删除字段 &ldquo;{field.name}&rdquo; 后，已有数据中该字段的值不会自动清除，但将无法在表单中编辑。
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel>取消</AlertDialogCancel>
                    <AlertDialogAction onClick={() => handleDelete(field.id)}>
                      确认删除
                    </AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
