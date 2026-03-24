export const GRADES = [
  { value: "A", label: "A 级 — 重点客户", color: "text-red-600" },
  { value: "B", label: "B 级 — 活跃客户", color: "text-orange-500" },
  { value: "C", label: "C 级 — 一般客户", color: "text-blue-500" },
  { value: "D", label: "D 级 — 低优先", color: "text-gray-400" },
] as const;

// Must match backend FollowUpMethod enum (api/app/domain/follow_up/enums.py)
export const FOLLOW_UP_METHODS = [
  { value: "phone", label: "电话", icon: "Phone" },
  { value: "email", label: "邮件", icon: "Mail" },
  { value: "wechat", label: "微信", icon: "MessageCircle" },
  { value: "whatsapp", label: "WhatsApp", icon: "MessageSquare" },
  { value: "alibaba", label: "阿里巴巴站内信", icon: "Store" },
  { value: "meeting", label: "会面", icon: "Users" },
  { value: "exhibition", label: "展会", icon: "Building" },
  { value: "other", label: "其他", icon: "MoreHorizontal" },
] as const;

export const QUOTATION_STATUSES = [
  { value: "draft", label: "草稿", variant: "secondary" },
  { value: "sent", label: "已发送", variant: "default" },
  { value: "following", label: "跟进中", variant: "accent" },
  { value: "confirmed", label: "已确认", variant: "success" },
  { value: "converted", label: "已转订单", variant: "success" },
  { value: "expired", label: "已过期", variant: "warning" },
  { value: "rejected", label: "已拒绝", variant: "destructive" },
] as const;

export const ORDER_STATUSES = [
  { value: "pending", label: "待确认", variant: "secondary" },
  { value: "confirmed", label: "已确认", variant: "default" },
  { value: "producing", label: "生产中", variant: "default" },
  { value: "ready_to_ship", label: "待发货", variant: "default" },
  { value: "shipping", label: "运输中", variant: "default" },
  { value: "delivered", label: "已送达", variant: "success" },
  { value: "completed", label: "已完成", variant: "success" },
  { value: "cancelled", label: "已取消", variant: "destructive" },
] as const;

export const PAYMENT_STATUSES = [
  { value: "unpaid", label: "未付款", variant: "destructive" },
  { value: "partial", label: "部分付款", variant: "warning" },
  { value: "paid", label: "已付清", variant: "success" },
] as const;

export type FollowUpMethodValue = (typeof FOLLOW_UP_METHODS)[number]["value"];

// Must match backend ScriptScene enum (api/app/domain/follow_up/enums.py)
export const SCRIPT_SCENES = [
  { value: "first_contact", label: "首次联系" },
  { value: "follow_up", label: "跟进回复" },
  { value: "quotation", label: "报价跟进" },
  { value: "sample", label: "样品跟进" },
  { value: "order_confirm", label: "订单确认" },
  { value: "after_sales", label: "售后跟进" },
  { value: "reactivation", label: "客户激活" },
] as const;

export type ScriptSceneValue = (typeof SCRIPT_SCENES)[number]["value"];

export type QuotationStatus = (typeof QUOTATION_STATUSES)[number]["value"];

export const QUOTATION_STATUS_MAP = Object.fromEntries(
  QUOTATION_STATUSES.map((s) => [s.value, s]),
) as Record<QuotationStatus, (typeof QUOTATION_STATUSES)[number]>;

export const QUOTATION_STATUS_TRANSITIONS: Record<QuotationStatus, QuotationStatus[]> = {
  draft: ["sent"],
  sent: ["following", "expired", "rejected"],
  following: ["confirmed", "expired", "rejected"],
  confirmed: ["converted"],
  converted: [],
  expired: [],
  rejected: [],
};

export const TRADE_TERMS = [
  { value: "FOB", label: "FOB \u2014 Free on Board" },
  { value: "CIF", label: "CIF \u2014 Cost, Insurance & Freight" },
  { value: "EXW", label: "EXW \u2014 Ex Works" },
  { value: "DDP", label: "DDP \u2014 Delivered Duty Paid" },
  { value: "CFR", label: "CFR \u2014 Cost & Freight" },
  { value: "FCA", label: "FCA \u2014 Free Carrier" },
] as const;

export const CURRENCIES = [
  { code: "USD", symbol: "$", name: "US Dollar" },
  { code: "EUR", symbol: "\u20AC", name: "Euro" },
  { code: "GBP", symbol: "\u00A3", name: "British Pound" },
  { code: "CNY", symbol: "\u00A5", name: "Chinese Yuan" },
  { code: "JPY", symbol: "\u00A5", name: "Japanese Yen" },
] as const;

export type OrderStatus = (typeof ORDER_STATUSES)[number]["value"];

export const ORDER_STATUS_MAP = Object.fromEntries(
  ORDER_STATUSES.map((s) => [s.value, s]),
) as Record<OrderStatus, (typeof ORDER_STATUSES)[number]>;

export const ORDER_STATUS_TRANSITIONS: Record<OrderStatus, OrderStatus[]> = {
  pending: ["confirmed"],
  confirmed: ["producing"],
  producing: ["ready_to_ship"],
  ready_to_ship: ["shipping"],
  shipping: ["delivered"],
  delivered: ["completed"],
  completed: [],
  cancelled: [],
};

export const ORDER_CANCELLABLE_STATUSES: OrderStatus[] = [
  "pending",
  "confirmed",
  "producing",
  "ready_to_ship",
];

export type PaymentStatus = (typeof PAYMENT_STATUSES)[number]["value"];

export const PAYMENT_STATUS_MAP = Object.fromEntries(
  PAYMENT_STATUSES.map((s) => [s.value, s]),
) as Record<PaymentStatus, (typeof PAYMENT_STATUSES)[number]>;
