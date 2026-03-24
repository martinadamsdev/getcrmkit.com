import { Input } from "@workspace/ui/components/input"
import { Label } from "@workspace/ui/components/label"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@workspace/ui/components/card"
import { Truck } from "lucide-react"

interface ShippingInfo {
  carrier: string
  domesticTrackingNo: string
  internationalTrackingNo: string
}

interface ShippingInfoCardProps extends ShippingInfo {
  onChange: (info: ShippingInfo) => void
  disabled: boolean
}

export function ShippingInfoCard({
  carrier,
  domesticTrackingNo,
  internationalTrackingNo,
  onChange,
  disabled,
}: ShippingInfoCardProps) {
  const update = (patch: Partial<ShippingInfo>) => {
    onChange({
      carrier,
      domesticTrackingNo,
      internationalTrackingNo,
      ...patch,
    })
  }

  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-base">
          <Truck className="h-4 w-4" />
          物流信息
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <Label>承运商</Label>
          <Input
            value={carrier}
            onChange={(e) => update({ carrier: e.target.value })}
            placeholder="如 DHL, UPS, 阿里巴巴物流"
            disabled={disabled}
            className="mt-1"
          />
        </div>
        <div>
          <Label>国内物流单号</Label>
          <Input
            value={domesticTrackingNo}
            onChange={(e) =>
              update({ domesticTrackingNo: e.target.value })
            }
            placeholder="工厂→仓库/港口"
            disabled={disabled}
            className="mt-1 font-mono"
          />
        </div>
        <div>
          <Label>国际物流单号</Label>
          <Input
            value={internationalTrackingNo}
            onChange={(e) =>
              update({ internationalTrackingNo: e.target.value })
            }
            placeholder="港口→客户"
            disabled={disabled}
            className="mt-1 font-mono"
          />
        </div>
      </CardContent>
    </Card>
  )
}
