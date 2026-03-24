import { test, expect } from "@playwright/test";

test.describe("Full CRM Regression", () => {
  test.beforeEach(async ({ page }) => {
    // Register and login
    await page.goto("/register");
    await page.fill('[name="email"]', `test-${Date.now()}@example.com`);
    await page.fill('[name="password"]', "TestPassword123!");
    await page.fill('[name="name"]', "Test User");
    await page.click('button[type="submit"]');
    await page.waitForURL("/");
  });

  test("complete workflow: customer -> follow-up -> product -> quotation -> order -> dashboard", async ({
    page,
  }) => {
    // Step 1: Create customer
    await page.goto("/customers");
    await page.click('button:has-text("新建")');
    await page.fill('[name="company_name"]', "E2E Test Corp");
    await page.selectOption('[name="country"]', "CN");
    await page.selectOption('[name="grade"]', "A");
    await page.click('button:has-text("确认")');
    await expect(page.locator("text=E2E Test Corp")).toBeVisible();

    // Step 2: Create follow-up for customer
    await page.goto("/follow-ups");
    await page.click('button:has-text("新建")');
    await page.fill('[name="content"]', "Initial contact via email");
    await page.click('button:has-text("确认")');
    await expect(
      page.locator("text=Initial contact via email"),
    ).toBeVisible();

    // Step 3: Create product
    await page.goto("/products");
    await page.click('button:has-text("新建")');
    await page.fill('[name="name"]', "Widget A");
    await page.fill('[name="sku"]', "WGT-001");
    await page.click('button:has-text("确认")');
    await expect(page.locator("text=Widget A")).toBeVisible();

    // Step 4: Create quotation
    await page.goto("/quotations/new");
    await page.click('button:has-text("选择客户")');
    await page.click("text=E2E Test Corp");
    await page.click('button:has-text("添加产品")');
    await page.click("text=Widget A");
    await page.fill('[name="quantity"]', "100");
    await page.click('button:has-text("保存")');
    await expect(page.locator("text=报价已创建")).toBeVisible();

    // Step 5: Verify profit calculation responds quickly
    const profitStart = Date.now();
    await page.waitForSelector('[data-testid="profit-panel"]');
    const profitDuration = Date.now() - profitStart;
    expect(profitDuration).toBeLessThan(100);

    // Step 6: Convert quotation to order
    await page.click('button:has-text("转为订单")');
    await page.click('button:has-text("确认")');
    await expect(page.locator("text=订单已创建")).toBeVisible();

    // Step 7: Verify dashboard reflects data
    await page.goto("/");
    const dashboardStart = Date.now();
    await page.waitForSelector("text=客户总数");
    const dashboardDuration = Date.now() - dashboardStart;
    expect(dashboardDuration).toBeLessThan(200);

    // Verify dashboard shows non-zero stats
    await expect(
      page.locator("text=客户总数").locator("..").locator("text=1"),
    ).toBeVisible();
  });
});
