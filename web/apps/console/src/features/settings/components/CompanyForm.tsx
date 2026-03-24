import { useForm } from "@tanstack/react-form"
import { Button } from "@workspace/ui/components/button"
import { Input } from "@workspace/ui/components/input"
import { Label } from "@workspace/ui/components/label"
import { Textarea } from "@workspace/ui/components/textarea"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@workspace/ui/components/select"
import { Card, CardContent } from "@workspace/ui/components/card"
import { toast } from "sonner"

import { FileUpload } from "@/shared/components/form/file-upload"
import { CURRENCIES } from "@/shared/lib/constants"

export function CompanyForm() {
  const form = useForm({
    defaultValues: {
      name: "",
      logo_url: "",
      address: "",
      bank_info: "",
      default_currency: "USD",
    },
    onSubmit: async () => {
      // TODO: Wire to PUT /company API
      toast.success("公司信息已保存")
    },
  })

  return (
    <div className="max-w-2xl space-y-6">
      <h2 className="text-2xl font-semibold">公司信息</h2>

      <Card>
        <CardContent className="space-y-6 pt-6">
          <div className="space-y-2">
            <Label htmlFor="logo">公司 Logo</Label>
            <FileUpload
              accept={{ "image/*": [] }}
              maxSize={5 * 1024 * 1024}
              onUpload={() => {
                // TODO: Upload file to S3 and set logo_url
              }}
            />
          </div>

          <form.Field
            name="name"
            validators={{
              onSubmit: ({ value }) => {
                if (!value.trim()) return "公司名称不能为空"
                return undefined
              },
            }}
          >
            {(field) => (
              <div className="space-y-2">
                <Label htmlFor="company_name">公司名称</Label>
                <Input
                  id="company_name"
                  aria-label="公司名称"
                  value={field.state.value}
                  onChange={(e) => field.handleChange(e.target.value)}
                  onBlur={field.handleBlur}
                />
                {field.state.meta.errors?.map((error) => (
                  <p key={String(error)} className="text-sm text-destructive">{String(error)}</p>
                ))}
              </div>
            )}
          </form.Field>

          <form.Field name="address">
            {(field) => (
              <div className="space-y-2">
                <Label htmlFor="address">公司地址</Label>
                <Textarea
                  id="address"
                  aria-label="公司地址"
                  rows={3}
                  value={field.state.value}
                  onChange={(e) => field.handleChange(e.target.value)}
                />
              </div>
            )}
          </form.Field>

          <form.Field name="bank_info">
            {(field) => (
              <div className="space-y-2">
                <Label htmlFor="bank_info">银行信息</Label>
                <Textarea
                  id="bank_info"
                  aria-label="银行信息"
                  rows={4}
                  placeholder={"银行名称\n账号\nSWIFT Code"}
                  value={field.state.value}
                  onChange={(e) => field.handleChange(e.target.value)}
                />
              </div>
            )}
          </form.Field>

          <form.Field name="default_currency">
            {(field) => (
              <div className="space-y-2">
                <Label htmlFor="currency">默认币种</Label>
                <Select value={field.state.value} onValueChange={field.handleChange}>
                  <SelectTrigger id="currency" aria-label="默认币种">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {CURRENCIES.map((c) => (
                      <SelectItem key={c.code} value={c.code}>
                        {c.symbol} {c.code} - {c.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            )}
          </form.Field>

          <div className="flex justify-end">
            <Button onClick={form.handleSubmit}>保存</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
