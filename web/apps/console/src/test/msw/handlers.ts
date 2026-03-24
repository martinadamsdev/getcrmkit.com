import { http, HttpResponse } from "msw"

export const handlers = [
  // Customer list
  http.get("/api/v1/customers", () => {
    return HttpResponse.json({
      items: [],
      total: 0,
      page: 1,
      page_size: 20,
    })
  }),
]
