import { useState } from "react"
import {
  Mail,
  Phone,
  Star,
  Plus,
  MessageSquare,
  Linkedin,
  Copy,
} from "lucide-react"
import { Badge } from "@workspace/ui/components/badge"
import { Button } from "@workspace/ui/components/button"
import { Card, CardContent } from "@workspace/ui/components/card"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@workspace/ui/components/tooltip"
import { EmptyState } from "@/shared/components/data/empty-state"
import { ContactCreateDialog } from "./contact-create-dialog"
import type { ContactResponse } from "../types"

type ContactListProps = {
  customerId: string
  contacts: ContactResponse[]
  onContactCreated?: () => void
}

function ChannelIcon({
  type,
  value,
}: {
  type: string
  value: string
}) {
  const handleClick = () => {
    if (type === "email") {
      window.open(`mailto:${value}`)
    } else if (type === "phone") {
      window.open(`tel:${value}`)
    } else {
      navigator.clipboard.writeText(value)
    }
  }

  const iconMap: Record<string, React.ReactNode> = {
    email: <Mail className="size-4 text-muted-foreground" />,
    phone: <Phone className="size-4 text-muted-foreground" />,
    whatsapp: <MessageSquare className="size-4 text-green-600" />,
    skype: <MessageSquare className="size-4 text-blue-500" />,
    linkedin: <Linkedin className="size-4 text-blue-600" />,
    wechat: <MessageSquare className="size-4 text-green-500" />,
  }

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <button
            type="button"
            className="rounded p-1 hover:bg-muted"
            onClick={handleClick}
            aria-label={`${type}: ${value}`}
          >
            {iconMap[type] ?? <Copy className="size-4" />}
          </button>
        </TooltipTrigger>
        <TooltipContent>{value}</TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}

export function ContactList({
  customerId,
  contacts,
  onContactCreated,
}: ContactListProps) {
  const [createDialogOpen, setCreateDialogOpen] = useState(false)

  if (contacts.length === 0) {
    return (
      <>
        <EmptyState
          icon={Mail}
          title="暂无联系人"
          description="添加联系人以管理客户沟通"
          action={{
            label: "添加联系人",
            onClick: () => setCreateDialogOpen(true),
          }}
        />
        <ContactCreateDialog
          customerId={customerId}
          open={createDialogOpen}
          onOpenChange={setCreateDialogOpen}
          onSuccess={onContactCreated}
        />
      </>
    )
  }

  return (
    <div className="flex flex-col gap-3">
      {contacts.map((contact) => {
        const channels = [
          contact.email && { type: "email", value: contact.email },
          contact.phone && { type: "phone", value: contact.phone },
          contact.whatsapp && { type: "whatsapp", value: contact.whatsapp },
          contact.skype && { type: "skype", value: contact.skype },
          contact.linkedin && { type: "linkedin", value: contact.linkedin },
          contact.wechat && { type: "wechat", value: contact.wechat },
        ].filter(Boolean) as { type: string; value: string }[]

        return (
          <Card key={contact.id}>
            <CardContent className="flex items-center justify-between p-4">
              <div className="flex flex-col gap-1">
                <div className="flex items-center gap-2">
                  <span className="font-medium">{contact.name}</span>
                  {contact.title && (
                    <span className="text-sm text-muted-foreground">
                      {contact.title}
                    </span>
                  )}
                  {contact.is_primary && (
                    <Badge variant="secondary" className="gap-1">
                      <Star className="size-3 fill-amber-400 text-amber-400" />
                      主要联系人
                    </Badge>
                  )}
                </div>
                {channels.length > 0 && (
                  <div className="flex items-center gap-1">
                    {channels.map((ch) => (
                      <ChannelIcon
                        key={ch.type}
                        type={ch.type}
                        value={ch.value}
                      />
                    ))}
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        )
      })}

      <Button
        variant="outline"
        className="w-full"
        onClick={() => setCreateDialogOpen(true)}
      >
        <Plus className="mr-2 size-4" />
        添加联系人
      </Button>

      <ContactCreateDialog
        customerId={customerId}
        open={createDialogOpen}
        onOpenChange={setCreateDialogOpen}
        onSuccess={onContactCreated}
      />
    </div>
  )
}
