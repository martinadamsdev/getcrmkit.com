import { Check, Copy } from "lucide-react";
import { Badge } from "@workspace/ui/components/badge";
import { Button } from "@workspace/ui/components/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@workspace/ui/components/card";
import { useCopyToClipboard } from "@/shared/hooks/use-copy-to-clipboard";
import { toast } from "sonner";

export interface ScriptTemplate {
  id: string;
  scene: string;
  title: string;
  content: string;
  language: string;
  position: number;
  is_system: boolean;
  created_at: string;
  updated_at: string;
}

interface ScriptCardProps {
  template: ScriptTemplate;
}

export function ScriptCard({ template }: ScriptCardProps) {
  const { copy, copied } = useCopyToClipboard();

  const handleCopy = async () => {
    const ok = await copy(template.content);
    if (ok) {
      toast.success("已复制到剪贴板");
    } else {
      toast.error("复制失败");
    }
  };

  return (
    <Card className="group">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">
          {template.title}
        </CardTitle>
        <div className="flex items-center gap-2">
          {template.is_system && (
            <Badge variant="secondary" className="text-xs">
              系统
            </Badge>
          )}
          <Button
            variant="ghost"
            size="icon"
            className="h-7 w-7"
            onClick={handleCopy}
            aria-label="复制"
          >
            {copied ? (
              <Check className="h-3.5 w-3.5" />
            ) : (
              <Copy className="h-3.5 w-3.5" />
            )}
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-xs text-muted-foreground line-clamp-3">
          {template.content}
        </p>
      </CardContent>
    </Card>
  );
}
