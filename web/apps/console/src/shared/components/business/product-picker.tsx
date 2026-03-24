import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { Check, ChevronsUpDown } from "lucide-react"
import { Button } from "@workspace/ui/components/button"
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@workspace/ui/components/command"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@workspace/ui/components/popover"
import { cn } from "@workspace/ui/lib/utils"
import { apiFetch } from "@/shared/api/fetcher"

interface ProductOption {
  id: string
  name: string
  sku: string | null
  selling_price: string | null
  selling_currency: string
}

interface ProductPickerProps {
  value: string | null
  onChange: (productId: string | null) => void
  className?: string
}

async function searchProducts(keyword: string): Promise<ProductOption[]> {
  const params = new URLSearchParams({ keyword, page_size: "20" })
  const res = await apiFetch(`/api/v1/products?${params}`)
  if (!res.ok) return []
  const data = await res.json()
  return data.items ?? []
}

export function ProductPicker({
  value,
  onChange,
  className,
}: ProductPickerProps) {
  const [open, setOpen] = useState(false)
  const [search, setSearch] = useState("")

  const { data: products = [] } = useQuery({
    queryKey: ["products-search", search],
    queryFn: () => searchProducts(search),
    enabled: open,
    staleTime: 10_000,
  })

  const selected = products.find((p) => p.id === value)

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className={cn("w-full justify-between font-normal", className)}
        >
          {selected ? (
            <span className="flex items-center gap-2 truncate">
              {selected.sku && (
                <span className="text-xs text-muted-foreground">
                  {selected.sku}
                </span>
              )}
              {selected.name}
              {selected.selling_price && (
                <span className="text-xs text-muted-foreground">
                  {selected.selling_currency} {selected.selling_price}
                </span>
              )}
            </span>
          ) : (
            <span className="text-muted-foreground">选择产品...</span>
          )}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[400px] p-0">
        <Command shouldFilter={false}>
          <CommandInput
            placeholder="搜索 SKU 或名称..."
            value={search}
            onValueChange={setSearch}
          />
          <CommandList>
            <CommandEmpty>未找到产品</CommandEmpty>
            <CommandGroup>
              {products.map((product) => (
                <CommandItem
                  key={product.id}
                  value={product.id}
                  onSelect={(id) => {
                    onChange(id === value ? null : id)
                    setOpen(false)
                  }}
                >
                  <Check
                    className={cn(
                      "mr-2 h-4 w-4",
                      value === product.id ? "opacity-100" : "opacity-0",
                    )}
                  />
                  <div className="flex flex-1 items-center gap-3">
                    <span className="text-xs text-muted-foreground w-20 shrink-0">
                      {product.sku ?? "\u2014"}
                    </span>
                    <span className="truncate">{product.name}</span>
                    {product.selling_price && (
                      <span className="ml-auto text-xs text-muted-foreground shrink-0">
                        {product.selling_currency} {product.selling_price}
                      </span>
                    )}
                  </div>
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
