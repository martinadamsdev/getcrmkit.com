import { useState } from "react"
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@workspace/ui/components/dialog"
import { Button } from "@workspace/ui/components/button"
import { Input } from "@workspace/ui/components/input"
import { Label } from "@workspace/ui/components/label"
import { Checkbox } from "@workspace/ui/components/checkbox"

type ContactFormData = {
  name: string
  title?: string
  email?: string
  phone?: string
  whatsapp?: string
  skype?: string
  linkedin?: string
  wechat?: string
  is_primary: boolean
  notes?: string
}

type ContactCreateDialogProps = {
  customerId: string
  open: boolean
  onOpenChange: (open: boolean) => void
  onSubmit?: (data: ContactFormData) => void
  onSuccess?: () => void
  isSubmitting?: boolean
}

export function ContactCreateDialog({
  open,
  onOpenChange,
  onSubmit,
  isSubmitting = false,
}: ContactCreateDialogProps) {
  const [name, setName] = useState("")
  const [title, setTitle] = useState("")
  const [email, setEmail] = useState("")
  const [phone, setPhone] = useState("")
  const [whatsapp, setWhatsapp] = useState("")
  const [skype, setSkype] = useState("")
  const [linkedin, setLinkedin] = useState("")
  const [wechat, setWechat] = useState("")
  const [isPrimary, setIsPrimary] = useState(false)
  const [notes, setNotes] = useState("")

  const resetForm = () => {
    setName("")
    setTitle("")
    setEmail("")
    setPhone("")
    setWhatsapp("")
    setSkype("")
    setLinkedin("")
    setWechat("")
    setIsPrimary(false)
    setNotes("")
  }

  const handleOpenChange = (isOpen: boolean) => {
    if (!isOpen) resetForm()
    onOpenChange(isOpen)
  }

  const handleSubmit = () => {
    if (!name.trim()) return
    onSubmit?.({
      name: name.trim(),
      title: title || undefined,
      email: email || undefined,
      phone: phone || undefined,
      whatsapp: whatsapp || undefined,
      skype: skype || undefined,
      linkedin: linkedin || undefined,
      wechat: wechat || undefined,
      is_primary: isPrimary,
      notes: notes || undefined,
    })
  }

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>添加联系人</DialogTitle>
        </DialogHeader>
        <div className="flex flex-col gap-4 py-4">
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="contact-name">
              姓名 <span className="text-destructive">*</span>
            </Label>
            <Input
              id="contact-name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="联系人姓名"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="contact-title">职位</Label>
            <Input
              id="contact-title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="如: 采购经理"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="contact-email">邮箱</Label>
              <Input
                id="contact-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="email@example.com"
              />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="contact-phone">电话</Label>
              <Input
                id="contact-phone"
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="+86 ..."
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="contact-whatsapp">WhatsApp</Label>
              <Input
                id="contact-whatsapp"
                value={whatsapp}
                onChange={(e) => setWhatsapp(e.target.value)}
                placeholder="WhatsApp 号码"
              />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="contact-skype">Skype</Label>
              <Input
                id="contact-skype"
                value={skype}
                onChange={(e) => setSkype(e.target.value)}
                placeholder="Skype ID"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="contact-linkedin">LinkedIn</Label>
              <Input
                id="contact-linkedin"
                value={linkedin}
                onChange={(e) => setLinkedin(e.target.value)}
                placeholder="LinkedIn URL"
              />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="contact-wechat">微信</Label>
              <Input
                id="contact-wechat"
                value={wechat}
                onChange={(e) => setWechat(e.target.value)}
                placeholder="微信号"
              />
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Checkbox
              id="contact-primary"
              checked={isPrimary}
              onCheckedChange={(checked) =>
                setIsPrimary(checked === true)
              }
            />
            <Label htmlFor="contact-primary">设为主要联系人</Label>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => handleOpenChange(false)}>
            取消
          </Button>
          <Button onClick={handleSubmit} disabled={!name.trim() || isSubmitting}>
            {isSubmitting ? "添加中..." : "添加"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
