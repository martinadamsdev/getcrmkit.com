import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@workspace/ui/components/select";
import { FOLLOW_UP_METHODS } from "@/shared/lib/constants";

interface FollowUpFiltersProps {
  method: string | undefined;
  onMethodChange: (method: string | undefined) => void;
  onReset: () => void;
}

export function FollowUpFilters({
  method,
  onMethodChange,
  onReset,
}: FollowUpFiltersProps) {
  return (
    <div className="flex items-center gap-3 border-b px-4 py-2">
      <Select
        value={method ?? "all"}
        onValueChange={(v) => onMethodChange(v === "all" ? undefined : v)}
      >
        <SelectTrigger className="w-[140px]">
          <SelectValue placeholder="跟进方式" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">全部方式</SelectItem>
          {FOLLOW_UP_METHODS.map((m) => (
            <SelectItem key={m.value} value={m.value}>
              {m.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      <button
        type="button"
        onClick={onReset}
        className="text-sm text-muted-foreground hover:text-foreground"
      >
        重置
      </button>
    </div>
  );
}
