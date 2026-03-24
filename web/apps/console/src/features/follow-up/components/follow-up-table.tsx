import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { format } from "date-fns";
import { Badge } from "@workspace/ui/components/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@workspace/ui/components/table";
import { FollowUpMethodIcon } from "./follow-up-method-icon";
import type { FollowUpMethodValue } from "@/shared/lib/constants";

export interface FollowUpRow {
  id: string;
  customer_id: string;
  customer_name: string;
  contact_id: string | null;
  method: string;
  stage: string | null;
  content: string;
  customer_response: string | null;
  next_follow_at: string | null;
  attachment_urls: string[];
  tags: string[];
  created_by: string | null;
  created_at: string;
  updated_at: string;
}

interface FollowUpTableProps {
  data: FollowUpRow[];
  total: number;
  page: number;
  pageSize: number;
  onPageChange: (page: number) => void;
}

const columnHelper = createColumnHelper<FollowUpRow>();

const columns = [
  columnHelper.accessor("customer_name", {
    header: "客户",
    cell: (info) => (
      <span className="font-medium">{info.getValue()}</span>
    ),
  }),
  columnHelper.accessor("method", {
    header: "方式",
    cell: (info) => (
      <FollowUpMethodIcon
        method={info.getValue() as FollowUpMethodValue}
      />
    ),
  }),
  columnHelper.accessor("content", {
    header: "内容",
    cell: (info) => (
      <span className="line-clamp-1 max-w-[300px] text-sm text-muted-foreground">
        {info.getValue()}
      </span>
    ),
  }),
  columnHelper.accessor("tags", {
    header: "标签",
    cell: (info) => (
      <div className="flex gap-1 flex-wrap">
        {info.getValue().map((tag) => (
          <Badge key={tag} variant="secondary" className="text-xs">
            {tag}
          </Badge>
        ))}
      </div>
    ),
  }),
  columnHelper.accessor("created_at", {
    header: "时间",
    cell: (info) => (
      <span className="text-sm text-muted-foreground">
        {format(new Date(info.getValue()), "yyyy-MM-dd HH:mm")}
      </span>
    ),
  }),
  columnHelper.accessor("next_follow_at", {
    header: "下次跟进",
    cell: (info) => {
      const val = info.getValue();
      if (!val) return <span className="text-muted-foreground/50">—</span>;
      const d = new Date(val);
      const isOverdue = d < new Date();
      return (
        <span
          className={
            isOverdue ? "text-destructive font-medium" : "text-sm"
          }
        >
          {format(d, "yyyy-MM-dd")}
        </span>
      );
    },
  }),
];

export function FollowUpTable({
  data,
  total,
  page,
  pageSize,
  onPageChange,
}: FollowUpTableProps) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  const totalPages = Math.ceil(total / pageSize);

  return (
    <div>
      <Table>
        <TableHeader>
          {table.getHeaderGroups().map((hg) => (
            <TableRow key={hg.id}>
              {hg.headers.map((h) => (
                <TableHead key={h.id}>
                  {h.isPlaceholder
                    ? null
                    : flexRender(
                        h.column.columnDef.header,
                        h.getContext(),
                      )}
                </TableHead>
              ))}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {table.getRowModel().rows.length === 0 ? (
            <TableRow>
              <TableCell
                colSpan={columns.length}
                className="h-24 text-center text-muted-foreground"
              >
                暂无跟进记录
              </TableCell>
            </TableRow>
          ) : (
            table.getRowModel().rows.map((row) => (
              <TableRow key={row.id}>
                {row.getVisibleCells().map((cell) => (
                  <TableCell key={cell.id}>
                    {flexRender(
                      cell.column.columnDef.cell,
                      cell.getContext(),
                    )}
                  </TableCell>
                ))}
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
      {totalPages > 1 && (
        <div className="flex items-center justify-between border-t px-4 py-3">
          <span className="text-sm text-muted-foreground">
            共 {total} 条
          </span>
          <div className="flex gap-1">
            <button
              type="button"
              disabled={page <= 1}
              onClick={() => onPageChange(page - 1)}
              className="rounded px-3 py-1 text-sm disabled:opacity-50"
            >
              上一页
            </button>
            <span className="px-3 py-1 text-sm">
              {page} / {totalPages}
            </span>
            <button
              type="button"
              disabled={page >= totalPages}
              onClick={() => onPageChange(page + 1)}
              className="rounded px-3 py-1 text-sm disabled:opacity-50"
            >
              下一页
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
