import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "@/shared/api/fetcher";
import type { DashboardData } from "../types";

export function useDashboard() {
  return useQuery<DashboardData>({
    queryKey: ["dashboard"],
    queryFn: async () => {
      const res = await apiFetch("/api/v1/dashboard");
      if (!res.ok) throw new Error("Failed to fetch dashboard");
      return res.json();
    },
    staleTime: 30_000, // 30s
    refetchInterval: 30_000,
  });
}
