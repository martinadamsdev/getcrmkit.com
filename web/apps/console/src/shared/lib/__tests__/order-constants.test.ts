import { describe, expect, it } from "vitest"
import {
  ORDER_STATUSES,
  ORDER_STATUS_TRANSITIONS,
  PAYMENT_STATUSES,
  ORDER_CANCELLABLE_STATUSES,
} from "../constants"

describe("ORDER_STATUSES", () => {
  it("has all 8 statuses", () => {
    expect(ORDER_STATUSES).toHaveLength(8)
    const values = ORDER_STATUSES.map((s) => s.value)
    expect(values).toEqual([
      "pending",
      "confirmed",
      "producing",
      "ready_to_ship",
      "shipping",
      "delivered",
      "completed",
      "cancelled",
    ])
  })

  it("each status has label and variant", () => {
    for (const status of ORDER_STATUSES) {
      expect(status).toHaveProperty("label")
      expect(status).toHaveProperty("variant")
    }
  })
})

describe("ORDER_STATUS_TRANSITIONS", () => {
  it("pending can transition to confirmed only (cancellation via ORDER_CANCELLABLE_STATUSES)", () => {
    expect(ORDER_STATUS_TRANSITIONS.pending).toEqual(["confirmed"])
  })

  it("confirmed can transition to producing only (cancellation via ORDER_CANCELLABLE_STATUSES)", () => {
    expect(ORDER_STATUS_TRANSITIONS.confirmed).toEqual(["producing"])
  })

  it("producing can transition to ready_to_ship only (cancellation via ORDER_CANCELLABLE_STATUSES)", () => {
    expect(ORDER_STATUS_TRANSITIONS.producing).toEqual(["ready_to_ship"])
  })

  it("ready_to_ship can transition to shipping only (cancellation via ORDER_CANCELLABLE_STATUSES)", () => {
    expect(ORDER_STATUS_TRANSITIONS.ready_to_ship).toEqual(["shipping"])
  })

  it("shipping can only transition to delivered (not cancellable)", () => {
    expect(ORDER_STATUS_TRANSITIONS.shipping).toEqual(["delivered"])
  })

  it("delivered can only transition to completed", () => {
    expect(ORDER_STATUS_TRANSITIONS.delivered).toEqual(["completed"])
  })

  it("completed is terminal", () => {
    expect(ORDER_STATUS_TRANSITIONS.completed).toEqual([])
  })

  it("cancelled is terminal", () => {
    expect(ORDER_STATUS_TRANSITIONS.cancelled).toEqual([])
  })
})

describe("PAYMENT_STATUSES", () => {
  it("has unpaid, partial, paid", () => {
    const values = PAYMENT_STATUSES.map((s) => s.value)
    expect(values).toEqual(["unpaid", "partial", "paid"])
  })

  it("unpaid is destructive", () => {
    expect(PAYMENT_STATUSES[0].variant).toBe("destructive")
  })

  it("partial is warning", () => {
    expect(PAYMENT_STATUSES[1].variant).toBe("warning")
  })

  it("paid is success", () => {
    expect(PAYMENT_STATUSES[2].variant).toBe("success")
  })
})

describe("ORDER_CANCELLABLE_STATUSES", () => {
  it("includes pending, confirmed, producing, ready_to_ship", () => {
    expect(ORDER_CANCELLABLE_STATUSES).toEqual([
      "pending",
      "confirmed",
      "producing",
      "ready_to_ship",
    ])
  })

  it("does not include shipping, delivered, completed", () => {
    expect(ORDER_CANCELLABLE_STATUSES).not.toContain("shipping")
    expect(ORDER_CANCELLABLE_STATUSES).not.toContain("delivered")
    expect(ORDER_CANCELLABLE_STATUSES).not.toContain("completed")
  })
})
