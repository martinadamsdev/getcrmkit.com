import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "@workspace/ui/components/button";
import { Calendar } from "@workspace/ui/components/calendar";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@workspace/ui/components/dialog";
import { Label } from "@workspace/ui/components/label";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@workspace/ui/components/popover";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@workspace/ui/components/select";
import { Textarea } from "@workspace/ui/components/textarea";
import { CalendarIcon } from "lucide-react";
import { format } from "date-fns";
import { toast } from "sonner";
import { cn } from "@workspace/ui/lib/utils";
import { FOLLOW_UP_METHODS } from "@/shared/lib/constants";
import { apiFetch } from "@/shared/api/fetcher";

interface FollowUpCreateDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

interface CreateFollowUpPayload {
  customer_id: string;
  method: string;
  content: string;
  customer_response?: string;
  next_follow_at?: string;
  attachment_urls: string[];
  tags: string[];
}

async function createFollowUp(payload: CreateFollowUpPayload) {
  const res = await apiFetch("/api/v1/follow-ups", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(
      (err as { detail?: { message?: string } }).detail?.message ??
        "创建失败",
    );
  }
  return res.json();
}

export function FollowUpCreateDialog({
  open,
  onOpenChange,
}: FollowUpCreateDialogProps) {
  const queryClient = useQueryClient();

  const [customerId, setCustomerId] = useState("");
  const [method, setMethod] = useState("email");
  const [content, setContent] = useState("");
  const [customerResponse, setCustomerResponse] = useState("");
  const [nextFollowAt, setNextFollowAt] = useState<Date | undefined>();
  const [tags, setTags] = useState<string[]>([]);
  const [tagInput, setTagInput] = useState("");

  const mutation = useMutation({
    mutationFn: createFollowUp,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["follow-ups"] });
      toast.success("跟进记录已创建");
      resetForm();
      onOpenChange(false);
    },
    onError: (err) => {
      toast.error(err.message);
    },
  });

  const resetForm = () => {
    setCustomerId("");
    setMethod("email");
    setContent("");
    setCustomerResponse("");
    setNextFollowAt(undefined);
    setTags([]);
    setTagInput("");
  };

  const handleSubmit = () => {
    if (!customerId || !content.trim()) {
      toast.error("请填写客户和跟进内容");
      return;
    }
    mutation.mutate({
      customer_id: customerId,
      method,
      content: content.trim(),
      customer_response: customerResponse.trim() || undefined,
      next_follow_at: nextFollowAt?.toISOString(),
      attachment_urls: [],
      tags,
    });
  };

  const handleAddTag = () => {
    const tag = tagInput.trim();
    if (tag && !tags.includes(tag)) {
      setTags([...tags, tag]);
      setTagInput("");
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[520px]">
        <DialogHeader>
          <DialogTitle>新建跟进记录</DialogTitle>
          <DialogDescription>记录与客户的沟通内容和反馈</DialogDescription>
        </DialogHeader>

        <div className="grid gap-4 py-4">
          {/* Customer Picker placeholder */}
          <div className="grid gap-2">
            <Label>客户</Label>
            <Select value={customerId} onValueChange={setCustomerId}>
              <SelectTrigger>
                <SelectValue placeholder="选择客户..." />
              </SelectTrigger>
              <SelectContent>
                {/* TODO: Replace with shared CustomerPicker component */}
              </SelectContent>
            </Select>
          </div>

          {/* Method select */}
          <div className="grid gap-2">
            <Label>跟进方式</Label>
            <Select value={method} onValueChange={setMethod}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {FOLLOW_UP_METHODS.map((m) => (
                  <SelectItem key={m.value} value={m.value}>
                    {m.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Content */}
          <div className="grid gap-2">
            <Label>跟进内容</Label>
            <Textarea
              placeholder="跟进内容..."
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={4}
            />
          </div>

          {/* Customer response */}
          <div className="grid gap-2">
            <Label>客户反馈</Label>
            <Textarea
              placeholder="客户反馈..."
              value={customerResponse}
              onChange={(e) => setCustomerResponse(e.target.value)}
              rows={2}
            />
          </div>

          {/* Next follow-up date */}
          <div className="grid gap-2">
            <Label>下次跟进日期</Label>
            <Popover>
              <PopoverTrigger asChild>
                <Button
                  variant="outline"
                  className={cn(
                    "justify-start text-left font-normal",
                    !nextFollowAt && "text-muted-foreground",
                  )}
                >
                  <CalendarIcon className="mr-2 h-4 w-4" />
                  {nextFollowAt
                    ? format(nextFollowAt, "yyyy-MM-dd")
                    : "选择日期"}
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-auto p-0">
                <Calendar
                  mode="single"
                  selected={nextFollowAt}
                  onSelect={setNextFollowAt}
                  initialFocus
                />
              </PopoverContent>
            </Popover>
          </div>

          {/* Tags */}
          <div className="grid gap-2">
            <Label>标签</Label>
            <div className="flex gap-2">
              <input
                className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
                placeholder="输入标签后回车..."
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault();
                    handleAddTag();
                  }
                }}
              />
            </div>
            {tags.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {tags.map((tag) => (
                  <span
                    key={tag}
                    className="inline-flex items-center gap-1 rounded-full bg-secondary px-2.5 py-0.5 text-xs"
                  >
                    {tag}
                    <button
                      type="button"
                      onClick={() =>
                        setTags(tags.filter((t) => t !== tag))
                      }
                      className="hover:text-destructive"
                    >
                      x
                    </button>
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            取消
          </Button>
          <Button onClick={handleSubmit} disabled={mutation.isPending}>
            {mutation.isPending ? "保存中..." : "保存"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
