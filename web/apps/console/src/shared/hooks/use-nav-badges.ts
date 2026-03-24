import { useQuery } from "@tanstack/react-query"
import { apiFetch } from "@/shared/api/fetcher"

interface NavBadges {
  customers: number
  quotations: number
  orders: number
  follow_ups: number
}

export function useNavBadges() {
  const { data } = useQuery<NavBadges>({
    queryKey: ["nav-badges"],
    queryFn: async () => {
      const res = await apiFetch("/api/v1/nav/badges")
      if (!res.ok) throw new Error("Failed to fetch badges")
      return res.json()
    },
    staleTime: 60_000,
    refetchInterval: 60_000,
  })

  return {
    customers: data?.customers ?? 0,
    quotations: data?.quotations ?? 0,
    orders: data?.orders ?? 0,
    follow_ups: data?.follow_ups ?? 0,
  }
}
