import { Input } from "@workspace/ui/components/input"
import { Label } from "@workspace/ui/components/label"
import { Switch } from "@workspace/ui/components/switch"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@workspace/ui/components/select"

export interface CustomFieldDef {
  id: string
  name: string
  type: "text" | "number" | "date" | "select" | "boolean"
  required: boolean
  options: string[]
}

interface DynamicFieldProps {
  definition: CustomFieldDef
  value: unknown
  onChange: (value: unknown) => void
}

export function DynamicField({ definition, value, onChange }: DynamicFieldProps) {
  const { id, name, type, required, options } = definition

  return (
    <div className="space-y-2">
      <Label htmlFor={id}>
        {name}
        {required && <span className="ml-1 text-destructive">*</span>}
      </Label>

      {type === "text" && (
        <Input
          id={id}
          aria-label={name}
          value={(value as string) ?? ""}
          onChange={(e) => onChange(e.target.value)}
        />
      )}

      {type === "number" && (
        <Input
          id={id}
          aria-label={name}
          type="number"
          value={(value as number) ?? 0}
          onChange={(e) => onChange(Number(e.target.value))}
        />
      )}

      {type === "date" && (
        <Input
          id={id}
          aria-label={name}
          type="date"
          value={(value as string) ?? ""}
          onChange={(e) => onChange(e.target.value)}
        />
      )}

      {type === "select" && (
        <Select value={(value as string) ?? ""} onValueChange={onChange}>
          <SelectTrigger id={id} aria-label={name}>
            <SelectValue placeholder={`选择${name}`} />
          </SelectTrigger>
          <SelectContent>
            {options.map((opt) => (
              <SelectItem key={opt} value={opt}>
                {opt}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      )}

      {type === "boolean" && (
        <Switch
          id={id}
          aria-label={name}
          checked={(value as boolean) ?? false}
          onCheckedChange={onChange}
        />
      )}
    </div>
  )
}
