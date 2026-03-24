import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@workspace/ui/components/alert-dialog"
import { Badge } from "@workspace/ui/components/badge"
import type { DuplicateMatch } from "../types"

type DuplicateWarningDialogProps = {
  open: boolean
  onOpenChange: (open: boolean) => void
  duplicates: DuplicateMatch[]
  onIgnore: () => void
  onViewExisting: (customerId: string) => void
}

export function DuplicateWarningDialog({
  open,
  onOpenChange,
  duplicates,
  onIgnore,
  onViewExisting,
}: DuplicateWarningDialogProps) {
  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>发现疑似重复客户</AlertDialogTitle>
          <AlertDialogDescription>
            以下客户与您输入的信息匹配：
          </AlertDialogDescription>
        </AlertDialogHeader>
        <div className="flex flex-col gap-2 py-2">
          {duplicates.map((dup) => (
            <div
              key={dup.customer_id}
              className="flex items-center justify-between rounded-md border p-3"
            >
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  className="font-medium text-primary hover:underline"
                  onClick={() => onViewExisting(dup.customer_id)}
                >
                  {dup.customer_name}
                </button>
                <Badge variant="secondary">{dup.match_type}</Badge>
              </div>
              <span className="text-sm text-muted-foreground">
                {dup.matched_value}
              </span>
            </div>
          ))}
        </div>
        <AlertDialogFooter>
          <AlertDialogCancel>取消</AlertDialogCancel>
          <AlertDialogAction onClick={onIgnore}>
            忽略并继续创建
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}
