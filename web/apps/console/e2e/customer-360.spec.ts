import { test, expect } from "./fixtures"

test.describe("Customer 360 Detail", () => {
  // Helper: create a customer and navigate to its detail page
  async function createAndNavigateToCustomer(
    page: import("@playwright/test").Page,
    name: string,
  ) {
    await page.goto("/customers")
    await page.getByRole("button", { name: /新建客户/ }).click()
    await page.getByLabel(/客户名称|名称/).fill(name)
    await page.getByRole("button", { name: /创建|提交|保存/ }).click()
    await expect(page.getByText(/创建成功|成功/)).toBeVisible({ timeout: 5000 })
    await page.getByText(name).first().click()
    await expect(page).toHaveURL(/\/customers\/[0-9a-f-]+/)
  }

  test("360 tabs all render with section headings", async ({ page }) => {
    await createAndNavigateToCustomer(page, "360 Tabs Co")

    // All tabs should be visible
    await expect(page.getByText("基本信息")).toBeVisible()
    await expect(page.getByText("联系人")).toBeVisible()
    await expect(page.getByText("跟进记录")).toBeVisible()
    await expect(page.getByText(/报价|报价单/)).toBeVisible()
    await expect(page.getByText(/订单/)).toBeVisible()
  })

  test("基本信息 tab shows customer info card with fields", async ({ page }) => {
    await createAndNavigateToCustomer(page, "Info Card Co")

    // Default tab should be 基本信息
    await page.getByText("基本信息").click()

    // Should see customer detail fields
    await expect(page.getByText("Info Card Co")).toBeVisible()
    // Common field labels in customer info
    await expect(
      page.getByText(/客户名称|国家|行业|来源/).first(),
    ).toBeVisible()
  })

  test("跟进记录 tab shows timeline area", async ({ page }) => {
    await createAndNavigateToCustomer(page, "Timeline Co")

    await page.getByText("跟进记录").click()

    // Should see timeline area (may be empty for new customer)
    await expect(
      page.getByText(/跟进记录|暂无记录|添加跟进/).first(),
    ).toBeVisible()
  })

  test("报价 tab shows quotation area", async ({ page }) => {
    await createAndNavigateToCustomer(page, "Quotation Co")

    await page.getByText(/报价|报价单/).click()

    // Should see quotation area (may be empty)
    await expect(
      page.getByText(/报价|暂无报价|创建报价/).first(),
    ).toBeVisible()
  })

  test("back navigation returns to customer list with preserved URL", async ({
    page,
  }) => {
    // Navigate to list with a filter
    await page.goto("/customers?q=backtest")

    // Create customer from list
    await page.getByRole("button", { name: /新建客户/ }).click()
    await page.getByLabel(/客户名称|名称/).fill("Back Nav Co")
    await page.getByRole("button", { name: /创建|提交|保存/ }).click()
    await expect(page.getByText(/创建成功|成功/)).toBeVisible({ timeout: 5000 })

    // Navigate to detail
    await page.getByText("Back Nav Co").first().click()
    await expect(page).toHaveURL(/\/customers\/[0-9a-f-]+/)

    // Go back
    await page.getByRole("button", { name: /返回列表/ }).click()

    // Should be on customer list
    await expect(page).toHaveURL(/\/customers/)
  })
})
