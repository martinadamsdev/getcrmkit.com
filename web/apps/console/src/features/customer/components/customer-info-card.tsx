import { Card, CardContent, CardHeader, CardTitle } from "@workspace/ui/components/card"
import { CountryFlag } from "@/shared/components/business/country-flag"
import type { CustomerResponse } from "../types"

type CustomerInfoCardProps = {
  customer: CustomerResponse
  className?: string
}

function InfoRow({ label, value }: { label: string; value?: React.ReactNode }) {
  return (
    <div className="flex flex-col gap-0.5">
      <span className="text-xs text-muted-foreground">{label}</span>
      <span className="text-sm">{value || "—"}</span>
    </div>
  )
}

export function CustomerInfoCard({ customer, className }: CustomerInfoCardProps) {
  const address = [customer.country, customer.region, customer.city, customer.address]
    .filter(Boolean)
    .join(", ")

  return (
    <div className={`flex flex-col gap-4 ${className ?? ""}`}>
      {/* Basic Info */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">基本信息</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <InfoRow label="行业" value={customer.industry} />
            <InfoRow label="来源" value={customer.source} />
            <InfoRow label="公司规模" value={customer.company_size} />
            <InfoRow
              label="网站"
              value={
                customer.website ? (
                  <a
                    href={customer.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary hover:underline"
                  >
                    {customer.website}
                  </a>
                ) : undefined
              }
            />
            <InfoRow
              label="地址"
              value={
                address ? (
                  <span>
                    <CountryFlag countryCode={customer.country} />
                    {" "}
                    {address}
                  </span>
                ) : undefined
              }
            />
          </div>
        </CardContent>
      </Card>

      {/* Background Info */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">采购背景</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <InfoRow label="主营产品" value={customer.main_products} />
            <InfoRow label="年采购量" value={customer.annual_volume} />
            <InfoRow label="现有供应商" value={customer.current_supplier} />
            <InfoRow label="决策流程" value={customer.decision_process} />
          </div>
        </CardContent>
      </Card>

      {/* Custom Fields */}
      {customer.custom_fields &&
        Object.keys(customer.custom_fields).length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="text-base">自定义字段</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4">
                {Object.entries(customer.custom_fields).map(([key, value]) => (
                  <InfoRow
                    key={key}
                    label={key}
                    value={value != null ? String(value) : undefined}
                  />
                ))}
              </div>
            </CardContent>
          </Card>
        )}
    </div>
  )
}
