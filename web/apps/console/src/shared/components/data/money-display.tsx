import { type HTMLAttributes, useMemo } from "react"
import { cn } from "@workspace/ui/lib/utils"

type MoneyDisplayProps = HTMLAttributes<HTMLSpanElement> & {
  amount: number
  currency?: string
  exchangeRate?: number
}

const CURRENCY_LOCALES: Record<string, string> = {
  USD: "en-US",
  EUR: "de-DE",
  GBP: "en-GB",
  CNY: "zh-CN",
  JPY: "ja-JP",
}

const ZERO_DECIMAL_CURRENCIES = ["JPY", "KRW", "VND"]

export function MoneyDisplay({
  amount,
  currency = "USD",
  exchangeRate,
  className,
  ...props
}: MoneyDisplayProps) {
  const formatted = useMemo(() => {
    const locale = CURRENCY_LOCALES[currency] ?? "en-US"
    const fractionDigits = ZERO_DECIMAL_CURRENCIES.includes(
      currency.toUpperCase(),
    )
      ? 0
      : 2
    return new Intl.NumberFormat(locale, {
      style: "currency",
      currency,
      minimumFractionDigits: fractionDigits,
      maximumFractionDigits: fractionDigits,
    }).format(amount)
  }, [amount, currency])

  return (
    <span className={cn("tabular-nums", className)} {...props}>
      {formatted}
      {exchangeRate != null && (
        <span className="ml-1 text-xs text-muted-foreground">
          ({"\u00D7"}{exchangeRate})
        </span>
      )}
    </span>
  )
}
