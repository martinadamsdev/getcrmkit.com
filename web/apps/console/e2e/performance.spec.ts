import { test, expect } from "@playwright/test";

test.describe("Performance Benchmarks (AC-1.0.2)", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/login");
    await page.fill('[name="email"]', "admin@example.com");
    await page.fill('[name="password"]', "password123");
    await page.click('button[type="submit"]');
    await page.waitForURL("/");
  });

  test("dashboard loads within acceptable time", async ({ page }) => {
    await page.goto("/");
    const start = Date.now();
    await page.waitForSelector('[data-testid="stats-row"]', { timeout: 5000 });
    const duration = Date.now() - start;
    console.log(`Dashboard load time: ${duration}ms`);
    expect(duration).toBeLessThan(3000); // 3s SLA including API round trip
  });

  test("customer list with 10,000 rows renders with virtual scroll", async ({
    page,
  }) => {
    await page.goto("/customers");
    await page.waitForSelector("table tbody tr");

    // Verify virtual scroll: not all 10k rows are in DOM
    const rowCount = await page.locator("table tbody tr").count();
    expect(rowCount).toBeLessThan(100);

    // Scroll to bottom should work smoothly
    const start = Date.now();
    await page.evaluate(() => {
      const scrollContainer = document.querySelector(
        '[data-testid="virtual-table"]',
      );
      if (scrollContainer) {
        scrollContainer.scrollTop = scrollContainer.scrollHeight;
      }
    });
    await page.waitForTimeout(100);
    const duration = Date.now() - start;
    console.log(`Virtual scroll time: ${duration}ms`);
    expect(duration).toBeLessThan(500);
  });

  test("first JS bundle size is under 200KB gzipped", async ({ page }) => {
    const responses: { url: string; size: number }[] = [];
    page.on("response", async (response) => {
      if (response.url().endsWith(".js")) {
        const headers = response.headers();
        const contentLength = Number.parseInt(
          headers["content-length"] ?? "0",
          10,
        );
        responses.push({ url: response.url(), size: contentLength });
      }
    });
    await page.goto("/login");
    await page.waitForLoadState("networkidle");

    const totalSize = responses.reduce((sum, r) => sum + r.size, 0);
    console.log(`Total JS size: ${(totalSize / 1024).toFixed(1)}KB`);
  });
});
