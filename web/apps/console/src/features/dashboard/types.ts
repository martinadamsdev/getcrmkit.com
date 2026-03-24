export interface DashboardStats {
  total_customers: number;
  total_quotations: number;
  quotation_conversion_rate: number; // percentage 0-100
  total_orders: number;
  pending_follow_ups: number; // overdue > 15 days
  delivery_alerts: number; // overdue + within 7 days
}

export interface SalesSummary {
  yearly_sales_usd: number;
  monthly_sales_usd: number;
}

export interface DeliveryAlert {
  order_id: string;
  order_number: string;
  customer_name: string;
  expected_date: string;
  status: "overdue" | "within_7_days";
}

export interface RecentQuotation {
  id: string;
  customer_name: string;
  product_name: string;
  amount: number;
  currency: string;
  status: string;
  created_at: string;
}

export interface OverdueFollowUp {
  customer_id: string;
  customer_name: string;
  days_since_last_follow_up: number;
}

export interface OrderDistributionItem {
  status: string;
  count: number;
}

export interface RecentOrder {
  id: string;
  order_number: string;
  customer_name: string;
  amount: number;
  currency: string;
  status: string;
  created_at: string;
}

export interface DashboardData {
  stats: DashboardStats;
  sales_summary: SalesSummary;
  delivery_alerts: DeliveryAlert[];
  recent_quotations: RecentQuotation[];
  overdue_follow_ups: OverdueFollowUp[];
  order_distribution: OrderDistributionItem[];
  recent_orders: RecentOrder[];
}
