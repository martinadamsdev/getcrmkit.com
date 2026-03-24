import { createClient } from "@hey-api/client-fetch"

export const client = createClient({
  baseUrl: "/api",
  headers: {
    "Content-Type": "application/json",
  },
})
