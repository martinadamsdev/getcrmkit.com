const COUNTRY_NAMES: Record<string, string> = {
  CN: "China",
  US: "United States",
  GB: "United Kingdom",
  DE: "Germany",
  FR: "France",
  JP: "Japan",
  KR: "South Korea",
  IN: "India",
  BR: "Brazil",
  RU: "Russia",
  AU: "Australia",
  CA: "Canada",
  IT: "Italy",
  ES: "Spain",
  MX: "Mexico",
  ID: "Indonesia",
  TH: "Thailand",
  VN: "Vietnam",
  MY: "Malaysia",
  SG: "Singapore",
  PH: "Philippines",
  AE: "United Arab Emirates",
  SA: "Saudi Arabia",
  TR: "Turkey",
  NL: "Netherlands",
  PL: "Poland",
  SE: "Sweden",
  NO: "Norway",
  DK: "Denmark",
  FI: "Finland",
  NZ: "New Zealand",
  ZA: "South Africa",
  EG: "Egypt",
  NG: "Nigeria",
  KE: "Kenya",
  AR: "Argentina",
  CL: "Chile",
  CO: "Colombia",
  PE: "Peru",
  PK: "Pakistan",
  BD: "Bangladesh",
}

function codeToFlag(code: string): string {
  return String.fromCodePoint(
    ...code
      .toUpperCase()
      .split("")
      .map((c) => 0x1f1e6 - 65 + c.charCodeAt(0)),
  )
}

type CountryFlagProps = {
  countryCode?: string | null
  showName?: boolean
  className?: string
}

export function CountryFlag({
  countryCode,
  showName = false,
  className,
}: CountryFlagProps) {
  if (!countryCode) return null

  const code = countryCode.toUpperCase()
  const flag = codeToFlag(code)
  const name = COUNTRY_NAMES[code] ?? code

  return (
    <span className={className} title={name}>
      {flag}
      {showName && <span className="ml-1">{name}</span>}
    </span>
  )
}
