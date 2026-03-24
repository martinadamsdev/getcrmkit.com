import { useState } from "react"
import { useForm } from "@tanstack/react-form"
import { Button } from "@workspace/ui/components/button"
import { Input } from "@workspace/ui/components/input"
import { Label } from "@workspace/ui/components/label"
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

const TIMEZONES = [
  { value: "Asia/Shanghai", label: "Asia/Shanghai (UTC+8)" },
  { value: "Asia/Hong_Kong", label: "Asia/Hong Kong (UTC+8)" },
  { value: "America/New_York", label: "America/New York (UTC-5)" },
  { value: "America/Los_Angeles", label: "America/Los Angeles (UTC-8)" },
  { value: "Europe/London", label: "Europe/London (UTC+0)" },
  { value: "Europe/Berlin", label: "Europe/Berlin (UTC+1)" },
  { value: "Asia/Tokyo", label: "Asia/Tokyo (UTC+9)" },
]

export function ProfileForm() {
  const [showPasswordChange, setShowPasswordChange] = useState(false)
  const [currentPassword, setCurrentPassword] = useState("")
  const [newPassword, setNewPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")

  const handlePasswordChange = () => {
    if (newPassword !== confirmPassword) {
      toast.error("两次密码输入不一致")
      return
    }
    // TODO: PUT /api/v1/auth/change-password
    toast.info("密码修改功能开发中")
  }

  const form = useForm({
    defaultValues: {
      name: "",
      email: "",
      timezone: "Asia/Shanghai",
      avatar_url: "",
    },
    onSubmit: async () => {
      // TODO: Wire to PUT /users/me API
      toast.success("个人信息已保存")
    },
  })

  return (
    <div className="max-w-2xl space-y-6">
      <h2 className="text-2xl font-semibold">个人信息</h2>

      <Card>
        <CardContent className="space-y-6 pt-6">
          {/* Avatar */}
          <div className="space-y-2">
            <Label htmlFor="avatar">头像</Label>
            <FileUpload
              accept={{ "image/*": [] }}
              maxSize={5 * 1024 * 1024}
              onUpload={() => {
                // TODO: Upload file to S3 and set avatar_url
              }}
            />
          </div>

          {/* Name */}
          <form.Field
            name="name"
            validators={{
              onSubmit: ({ value }) => {
                if (!value.trim()) return "姓名不能为空"
                return undefined
              },
            }}
          >
            {(field) => (
              <div className="space-y-2">
                <Label htmlFor="name">姓名</Label>
                <Input
                  id="name"
                  aria-label="姓名"
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

          {/* Email (read-only) */}
          <form.Field name="email">
            {(field) => (
              <div className="space-y-2">
                <Label htmlFor="email">邮箱</Label>
                <Input
                  id="email"
                  aria-label="邮箱"
                  value={field.state.value}
                  disabled
                  className="bg-muted"
                />
              </div>
            )}
          </form.Field>

          {/* Timezone */}
          <form.Field name="timezone">
            {(field) => (
              <div className="space-y-2">
                <Label htmlFor="timezone">时区</Label>
                <Select value={field.state.value} onValueChange={field.handleChange}>
                  <SelectTrigger id="timezone" aria-label="时区">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {TIMEZONES.map((tz) => (
                      <SelectItem key={tz.value} value={tz.value}>
                        {tz.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            )}
          </form.Field>

          {/* Password Change Toggle */}
          <div>
            <Button
              type="button"
              variant="outline"
              onClick={() => setShowPasswordChange(!showPasswordChange)}
            >
              {showPasswordChange ? "取消修改密码" : "修改密码"}
            </Button>
          </div>

          {showPasswordChange && (
            <div className="space-y-4 rounded-md border border-border p-4">
              <div className="space-y-2">
                <Label htmlFor="current_password">当前密码</Label>
                <Input
                  id="current_password"
                  aria-label="当前密码"
                  type="password"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="new_password">新密码</Label>
                <Input
                  id="new_password"
                  aria-label="新密码"
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="confirm_password">确认密码</Label>
                <Input
                  id="confirm_password"
                  aria-label="确认密码"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
              </div>
              <div className="flex justify-end">
                <Button
                  type="button"
                  onClick={handlePasswordChange}
                  disabled={!currentPassword || !newPassword || newPassword !== confirmPassword}
                >
                  修改密码
                </Button>
              </div>
            </div>
          )}

          {/* Save */}
          <div className="flex justify-end">
            <Button onClick={form.handleSubmit}>保存</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
