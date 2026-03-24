import { useState } from "react"
import { X } from "lucide-react"
import { HexColorPicker } from "react-colorful"
import { Badge } from "@workspace/ui/components/badge"
import { Input } from "@workspace/ui/components/input"
import { Button } from "@workspace/ui/components/button"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@workspace/ui/components/popover"

export type Tag = { id?: string; name: string; color: string }

type TagInputProps = {
  tags: Tag[]
  suggestions?: Tag[]
  onAdd: (tag: { name: string; color: string }) => void
  onRemove: (index: number) => void
  className?: string
}

const DEFAULT_COLOR = "#6366f1"

export function TagInput({
  tags,
  onAdd,
  onRemove,
  className,
}: TagInputProps) {
  const [inputValue, setInputValue] = useState("")
  const [selectedColor, setSelectedColor] = useState(DEFAULT_COLOR)

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && inputValue.trim()) {
      e.preventDefault()
      onAdd({ name: inputValue.trim(), color: selectedColor })
      setInputValue("")
    }
  }

  return (
    <div className={`flex flex-wrap items-center gap-2 ${className ?? ""}`}>
      {tags.map((tag, index) => (
        <Badge key={tag.id ?? `${tag.name}-${index}`} variant="secondary">
          <span
            className="mr-1 inline-block size-2 rounded-full"
            style={{ backgroundColor: tag.color }}
          />
          {tag.name}
          <button
            type="button"
            aria-label={`Remove ${tag.name}`}
            onClick={() => onRemove(index)}
            className="ml-1 rounded-sm opacity-70 hover:opacity-100"
          >
            <X className="size-3" />
          </button>
        </Badge>
      ))}
      <div className="flex items-center gap-1">
        <Popover>
          <PopoverTrigger asChild>
            <Button
              type="button"
              variant="ghost"
              size="icon"
              aria-label="Pick color"
              className="size-6"
            >
              <span
                className="size-4 rounded-full border"
                style={{ backgroundColor: selectedColor }}
              />
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-auto p-3">
            <HexColorPicker color={selectedColor} onChange={setSelectedColor} />
          </PopoverContent>
        </Popover>
        <Input
          placeholder="Add tag..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          className="h-7 w-24"
        />
      </div>
    </div>
  )
}
