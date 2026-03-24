import {
  Building2,
  Mail,
  MessageCircle,
  MessageSquare,
  MoreHorizontal,
  Phone,
  Store,
  Users,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { cn } from "@workspace/ui/lib/utils";
import { FOLLOW_UP_METHODS } from "@/shared/lib/constants";
import type { FollowUpMethodValue } from "@/shared/lib/constants";

const ICON_MAP: Record<
  FollowUpMethodValue,
  { icon: LucideIcon; color: string }
> = {
  email: { icon: Mail, color: "text-blue-600" },
  phone: { icon: Phone, color: "text-green-600" },
  wechat: { icon: MessageCircle, color: "text-emerald-600" },
  whatsapp: { icon: MessageSquare, color: "text-green-500" },
  alibaba: { icon: Store, color: "text-orange-600" },
  meeting: { icon: Users, color: "text-purple-600" },
  exhibition: { icon: Building2, color: "text-amber-600" },
  other: { icon: MoreHorizontal, color: "text-muted-foreground" },
};

interface FollowUpMethodIconProps {
  method: FollowUpMethodValue;
  className?: string;
  size?: number;
}

export function FollowUpMethodIcon({
  method,
  className,
  size = 16,
}: FollowUpMethodIconProps) {
  const config = ICON_MAP[method] ?? ICON_MAP.other;
  const Icon = config.icon;
  const label =
    FOLLOW_UP_METHODS.find((m) => m.value === method)?.label ?? "其他";

  return (
    <span
      className={cn(config.color, className)}
      aria-label={label}
      role="img"
    >
      <Icon size={size} />
    </span>
  );
}
