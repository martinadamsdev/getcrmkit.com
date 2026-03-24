import { Filter, Plus, Search } from "lucide-react";
import { Button } from "@workspace/ui/components/button";
import { Input } from "@workspace/ui/components/input";

interface FollowUpToolbarProps {
  onSearch: (query: string) => void;
  onCreateClick: () => void;
  onFilterToggle: () => void;
  filtersOpen: boolean;
}

export function FollowUpToolbar({
  onSearch,
  onCreateClick,
  onFilterToggle,
  filtersOpen,
}: FollowUpToolbarProps) {
  return (
    <div className="flex items-center justify-between gap-4 px-4 py-3">
      <div className="flex items-center gap-2 flex-1 max-w-sm">
        <div className="relative flex-1">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="搜索跟进记录..."
            className="pl-8"
            onChange={(e) => onSearch(e.target.value)}
          />
        </div>
        <Button
          variant={filtersOpen ? "secondary" : "outline"}
          size="icon"
          onClick={onFilterToggle}
          aria-label="筛选"
        >
          <Filter className="h-4 w-4" />
        </Button>
      </div>
      <Button onClick={onCreateClick}>
        <Plus className="mr-1.5 h-4 w-4" />
        新建跟进
      </Button>
    </div>
  );
}
