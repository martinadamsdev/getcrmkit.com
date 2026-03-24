// Customer feature types — mirrors API response shapes
// These will eventually be auto-generated from OpenAPI spec

export type GradeResponse = {
  id: string
  name: string
  color: string
  position: number
}

export type TagResponse = {
  id: string
  name: string
  color: string
}

export type ContactResponse = {
  id: string
  customer_id: string
  name: string
  title?: string | null
  email?: string | null
  phone?: string | null
  whatsapp?: string | null
  skype?: string | null
  linkedin?: string | null
  wechat?: string | null
  is_primary: boolean
  notes?: string | null
  created_at: string
  updated_at: string
}

export type CustomerResponse = {
  id: string
  name: string
  country?: string | null
  region?: string | null
  city?: string | null
  address?: string | null
  industry?: string | null
  source?: string | null
  company_size?: string | null
  website?: string | null
  main_products?: string | null
  annual_volume?: string | null
  current_supplier?: string | null
  decision_process?: string | null
  background_info?: string | null
  custom_fields?: Record<string, unknown> | null
  grade?: GradeResponse | null
  tags: TagResponse[]
  contacts: ContactResponse[]
  contact_count: number
  last_follow_at?: string | null
  follow_status?: string | null
  created_at: string
  updated_at: string
}

export type CustomerListResponse = {
  items: CustomerResponse[]
  total: number
  page: number
  page_size: number
}

export type DuplicateMatch = {
  customer_id: string
  customer_name: string
  match_type: string
  matched_value: string
}

export type FollowUpItem = {
  id: string
  customer_id: string
  method: string
  content: string
  stage?: string | null
  attachment_count: number
  created_at: string
  created_by?: string | null
}

export type QuotationSummary = {
  id: string
  quotation_no: string
  customer_id: string
  total_amount: number
  currency: string
  trade_terms?: string | null
  status: string
  created_at: string
}

export type QuotationLineItem = {
  id: string
  product_name: string
  quantity: number
  unit_price: number
  amount: number
}

export type QuotationDetail = {
  id: string
  quotation_no: string
  customer_name: string
  total_amount: number
  currency: string
  trade_terms?: string | null
  status: string
  line_items: QuotationLineItem[]
  created_at: string
}

export type Customer360Response = {
  customer: CustomerResponse
  stats: {
    contact_count: number
    follow_up_count: number
    quotation_count: number
    order_count: number
  }
  recent_follow_ups: FollowUpItem[]
  quotations: QuotationSummary[]
}

export type SavedView = {
  id: string
  name: string
  entity: string
  filter_config: Record<string, string | null>
  created_at: string
}

export type CustomerFilters = {
  grade_id?: string | null
  source?: string | null
  country?: string | null
  industry?: string | null
  tag_ids?: string[] | null
  follow_status?: string | null
}
