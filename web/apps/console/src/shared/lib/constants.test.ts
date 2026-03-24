import { describe, it, expect } from "vitest";
import {
  GRADES,
  FOLLOW_UP_METHODS,
  QUOTATION_STATUSES,
  ORDER_STATUSES,
  PAYMENT_STATUSES,
} from "./constants";

describe("GRADES", () => {
  it("contains A/B/C/D", () => {
    const values = GRADES.map((g) => g.value);
    expect(values).toEqual(["A", "B", "C", "D"]);
  });

  it("each grade has label and color", () => {
    for (const grade of GRADES) {
      expect(grade).toHaveProperty("label");
      expect(grade).toHaveProperty("value");
      expect(grade).toHaveProperty("color");
    }
  });
});

describe("FOLLOW_UP_METHODS", () => {
  it("contains all 8 methods from spec", () => {
    const values = FOLLOW_UP_METHODS.map((m) => m.value);
    expect(values).toContain("email");
    expect(values).toContain("phone");
    expect(values).toContain("wechat");
    expect(values).toContain("whatsapp");
    expect(values).toContain("alibaba");
    expect(values).toContain("exhibition");
    expect(values).toContain("meeting");
    expect(values).toContain("other");
    expect(values).toHaveLength(8);
  });

  it("each method has label and icon", () => {
    for (const method of FOLLOW_UP_METHODS) {
      expect(method).toHaveProperty("label");
      expect(method).toHaveProperty("value");
      expect(method).toHaveProperty("icon");
    }
  });
});

describe("QUOTATION_STATUSES", () => {
  it("contains all 7 statuses from spec", () => {
    const values = QUOTATION_STATUSES.map((s) => s.value);
    expect(values).toEqual([
      "draft",
      "sent",
      "following",
      "confirmed",
      "converted",
      "expired",
      "rejected",
    ]);
  });

  it("each status has label and variant", () => {
    for (const status of QUOTATION_STATUSES) {
      expect(status).toHaveProperty("label");
      expect(status).toHaveProperty("value");
      expect(status).toHaveProperty("variant");
    }
  });
});

describe("ORDER_STATUSES", () => {
  it("contains all 8 statuses from spec", () => {
    const values = ORDER_STATUSES.map((s) => s.value);
    expect(values).toEqual([
      "pending",
      "confirmed",
      "producing",
      "ready_to_ship",
      "shipping",
      "delivered",
      "completed",
      "cancelled",
    ]);
  });
});

describe("PAYMENT_STATUSES", () => {
  it("contains unpaid/partial/paid", () => {
    const values = PAYMENT_STATUSES.map((s) => s.value);
    expect(values).toEqual(["unpaid", "partial", "paid"]);
  });

  it("has correct color mapping", () => {
    const unpaid = PAYMENT_STATUSES.find((s) => s.value === "unpaid");
    const partial = PAYMENT_STATUSES.find((s) => s.value === "partial");
    const paid = PAYMENT_STATUSES.find((s) => s.value === "paid");
    expect(unpaid?.variant).toBe("destructive");
    expect(partial?.variant).toBe("warning");
    expect(paid?.variant).toBe("success");
  });
});
