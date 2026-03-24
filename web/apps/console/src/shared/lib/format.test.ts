import { describe, it, expect } from "vitest";
import { formatMoney, formatDate, formatRelativeTime } from "./format";

describe("formatMoney", () => {
  it("formats USD with 2 decimals", () => {
    expect(formatMoney(1234.5, "USD")).toBe("$1,234.50");
  });

  it("formats CNY with symbol", () => {
    expect(formatMoney(9999, "CNY")).toBe("¥9,999.00");
  });

  it("formats EUR", () => {
    expect(formatMoney(1000, "EUR")).toContain("1,000.00");
  });

  it("handles zero", () => {
    expect(formatMoney(0, "USD")).toBe("$0.00");
  });

  it("handles negative values", () => {
    const result = formatMoney(-500, "USD");
    expect(result).toContain("500.00");
  });
});

describe("formatDate", () => {
  it("formats date to yyyy-MM-dd by default", () => {
    const date = new Date("2026-03-23T10:00:00Z");
    expect(formatDate(date)).toBe("2026-03-23");
  });

  it("formats date with custom format", () => {
    const date = new Date("2026-03-23T10:00:00Z");
    expect(formatDate(date, "yyyy/MM/dd")).toBe("2026/03/23");
  });

  it("formats datetime", () => {
    const date = new Date("2026-03-23T10:30:00Z");
    const result = formatDate(date, "yyyy-MM-dd HH:mm");
    expect(result).toContain("2026-03-23");
  });

  it("handles string input", () => {
    expect(formatDate("2026-03-23")).toBe("2026-03-23");
  });
});

describe("formatRelativeTime", () => {
  it("returns '刚刚' for recent times", () => {
    const now = new Date();
    expect(formatRelativeTime(now)).toBe("刚刚");
  });

  it("returns minutes ago", () => {
    const fiveMinAgo = new Date(Date.now() - 5 * 60 * 1000);
    expect(formatRelativeTime(fiveMinAgo)).toBe("5 分钟前");
  });

  it("returns hours ago", () => {
    const twoHoursAgo = new Date(Date.now() - 2 * 60 * 60 * 1000);
    expect(formatRelativeTime(twoHoursAgo)).toBe("2 小时前");
  });

  it("returns days ago", () => {
    const threeDaysAgo = new Date(Date.now() - 3 * 24 * 60 * 60 * 1000);
    expect(formatRelativeTime(threeDaysAgo)).toBe("3 天前");
  });
});
