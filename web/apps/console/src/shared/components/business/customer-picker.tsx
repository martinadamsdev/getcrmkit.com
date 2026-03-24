import { useState, useEffect } from "react"
import { useQuery } from "@tanstack/react-query"
import { ChevronsUpDown } from "lucide-react"
import { Button } from "@workspace/ui/components/button"
import { Input } from "@workspace/ui/components/input"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@workspace/ui/components/popover"
import { useDebounce } from "@/shared/hooks/use-debounce"
import { CountryFlag } from "./country-flag"
import { apiFetch } from "@/shared/api/fetcher"

type CustomerResult = {
  id: string
  company_name: string
  country?: string
  grade?: string
}

type CustomerPickerProps = {
  value?: string
  displayName?: string
  onChange: (customerId: string, customerName: string) => void
  className?: string
}

export function CustomerPicker({
  value,
  displayName,
  onChange,
  className,
}: CustomerPickerProps) {
  const [open, setOpen] = useState(false)
  const [search, setSearch] = useState("")
  const debouncedSearch = useDebounce(search, 300)

  const { data, isLoading } = useQuery({
    queryKey: ["customers", "picker", debouncedSearch],
    queryFn: async () => {
      const params = new URLSearchParams({ page_size: "10" })
      if (debouncedSearch) params.set("keyword", debouncedSearch)
      const res = await apiFetch(`/api/v1/customers?${params}`)
      if (!res.ok) throw new Error("Failed to fetch customers")
      return res.json() as Promise<{ items: CustomerResult[]; total: number }>
    },
    enabled: open,
  })

  const customers = data?.items ?? []

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button variant="outline" className={className}>
          {displayName || (value ? "Loading..." : "Select customer")}
          <ChevronsUpDown className="ml-2 size-4 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-72 p-0">
        <div className="p-2">
          <Input
            placeholder="Search customers..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <div className="max-h-60 overflow-y-auto">
          {isLoading ? (
            <div className="py-6 text-center text-sm text-muted-foreground">
              Loading...
            </div>
          ) : customers.length === 0 ? (
            <div className="py-6 text-center text-sm text-muted-foreground">
              No customers found
            </div>
          ) : (
            customers.map((customer) => (
              <button
                key={customer.id}
                type="button"
                className="flex w-full items-center gap-2 px-3 py-2 text-sm hover:bg-muted"
                onClick={() => {
                  onChange(customer.id, customer.company_name)
                  setOpen(false)
                }}
              >
                <CountryFlag countryCode={customer.country} />
                <span className="flex-1 text-left">
                  {customer.company_name}
                </span>
                {customer.grade && (
                  <span className="text-xs text-muted-foreground">
                    {customer.grade}
                  </span>
                )}
              </button>
            ))
          )}
        </div>
      </PopoverContent>
    </Popover>
  )
}
