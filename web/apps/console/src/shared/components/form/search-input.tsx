import { useEffect, useState } from "react"
import { Search, X } from "lucide-react"
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from "@workspace/ui/components/input-group"
import { useDebounce } from "@/shared/hooks/use-debounce"

type SearchInputProps = {
  placeholder?: string
  onSearch: (value: string) => void
  debounceMs?: number
  defaultValue?: string
  className?: string
}

export function SearchInput({
  placeholder = "Search...",
  onSearch,
  debounceMs = 500,
  defaultValue = "",
  className,
}: SearchInputProps) {
  const [value, setValue] = useState(defaultValue)
  const debouncedValue = useDebounce(value, debounceMs)

  useEffect(() => {
    onSearch(debouncedValue)
  }, [debouncedValue, onSearch])

  return (
    <InputGroup className={className}>
      <InputGroupAddon align="inline-start">
        <Search className="size-4" />
      </InputGroupAddon>
      <InputGroupInput
        placeholder={placeholder}
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
      {value && (
        <InputGroupAddon align="inline-end">
          <InputGroupButton
            aria-label="clear"
            onClick={() => setValue("")}
            size="icon-xs"
          >
            <X className="size-3" />
          </InputGroupButton>
        </InputGroupAddon>
      )}
    </InputGroup>
  )
}
