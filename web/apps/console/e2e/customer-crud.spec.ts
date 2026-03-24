import { test, expect } from "./fixtures"

test.describe("Customer CRUD", () => {
  test("customer list page loads with toolbar", async ({ page }) => {
    await page.goto("/customers")

    await expect(page.getByText("客户管理")).toBeVisible()
    await expect(
      page.getByPlaceholder(/搜索客户名|搜索/),
    ).toBeVisible()
    await expect(
      page.getByRole("button", { name: /新建客户/ }),
    ).toBeVisible()
  })

  test("create customer flow", async ({ page }) => {
    await page.goto("/customers")
    await page.getByRole("button", { name: /新建客户/ }).click()

    // Dialog should appear
    await expect(page.getByText(/新建客户|创建客户/)).toBeVisible()

    // Fill form
    await page.getByLabel(/客户名称|名称/).fill("E2E Test Company")

    // Submit
    await page.getByRole("button", { name: /创建|提交|保存/ }).click()

    // Success feedback
    await expect(page.getByText(/创建成功|成功/)).toBeVisible({ timeout: 5000 })
    await expect(page.getByText("E2E Test Company")).toBeVisible({
      timeout: 5000,
    })
  })

  test("duplicate check shows warning", async ({ page }) => {
    await page.goto("/customers")

    // Create first customer
    await page.getByRole("button", { name: /新建客户/ }).click()
    await page.getByLabel(/客户名称|名称/).fill("Duplicate Check Co")
    await page.getByRole("button", { name: /创建|提交|保存/ }).click()
    await expect(page.getByText(/创建成功|成功/)).toBeVisible({ timeout: 5000 })

    // Try creating another with same name
    await page.getByRole("button", { name: /新建客户/ }).click()
    await page.getByLabel(/客户名称|名称/).fill("Duplicate Check Co")

    // Wait for debounced duplicate check
    await page.waitForTimeout(600)

    // Should show duplicate warning
    await expect(
      page.getByText(/疑似重复|重复客户|已存在/),
    ).toBeVisible({ timeout: 5000 })
  })

  test("click customer row navigates to 360 detail", async ({ page }) => {
    await page.goto("/customers")

    // Create a customer first
    await page.getByRole("button", { name: /新建客户/ }).click()
    await page.getByLabel(/客户名称|名称/).fill("Detail View Co")
    await page.getByRole("button", { name: /创建|提交|保存/ }).click()
    await expect(page.getByText(/创建成功|成功/)).toBeVisible({ timeout: 5000 })

    // Click on the customer row
    await page.getByText("Detail View Co").click()

    // Should navigate to detail page
    await expect(page).toHaveURL(/\/customers\/[0-9a-f-]+/)
    await expect(page.getByText("基本信息")).toBeVisible({ timeout: 5000 })
    await expect(page.getByText("联系人")).toBeVisible()
  })

  test("add contact on detail page", async ({ page }) => {
    await page.goto("/customers")

    // Create customer
    await page.getByRole("button", { name: /新建客户/ }).click()
    await page.getByLabel(/客户名称|名称/).fill("Contact Test Co")
    await page.getByRole("button", { name: /创建|提交|保存/ }).click()
    await expect(page.getByText(/创建成功|成功/)).toBeVisible({ timeout: 5000 })

    // Navigate to detail
    await page.getByText("Contact Test Co").first().click()
    await expect(page).toHaveURL(/\/customers\/[0-9a-f-]+/)

    // Switch to contacts tab
    await page.getByText("联系人").click()

    // Add contact
    await page.getByRole("button", { name: /添加联系人/ }).click()
    await page.getByLabel(/姓名|名称/).fill("John Doe")
    await page.getByLabel(/邮箱/).fill("john@example.com")
    await page.getByRole("button", { name: /创建|提交|保存/ }).click()

    // Verify contact appears
    await expect(page.getByText("John Doe")).toBeVisible({ timeout: 5000 })
  })

  test("filter customers by grade", async ({ page }) => {
    await page.goto("/customers")

    // Open filter panel
    await page.getByRole("button", { name: /筛选|过滤/ }).click()

    // Select grade A
    await page.getByText("A").click()

    // URL should update with filter param
    await expect(page).toHaveURL(/grade_id=/, { timeout: 5000 })
  })

  test("search customers by keyword", async ({ page }) => {
    await page.goto("/customers")

    // Type in search
    await page
      .getByPlaceholder(/搜索客户名|搜索/)
      .fill("E2E Test")

    // Wait for debounce
    await page.waitForTimeout(600)

    // URL should update with search param
    await expect(page).toHaveURL(/q=E2E/, { timeout: 5000 })
  })

  test("view customer detail with 360 tabs", async ({ page }) => {
    await page.goto("/customers")

    // Create customer
    await page.getByRole("button", { name: /新建客户/ }).click()
    await page.getByLabel(/客户名称|名称/).fill("360 View Co")
    await page.getByRole("button", { name: /创建|提交|保存/ }).click()
    await expect(page.getByText(/创建成功|成功/)).toBeVisible({ timeout: 5000 })

    // Navigate to detail
    await page.getByText("360 View Co").first().click()
    await expect(page).toHaveURL(/\/customers\/[0-9a-f-]+/)

    // Check tabs exist
    await expect(page.getByText("基本信息")).toBeVisible()
    await expect(page.getByText("联系人")).toBeVisible()
    await expect(page.getByText("跟进记录")).toBeVisible()
  })

  test("navigate between tabs on detail page", async ({ page }) => {
    await page.goto("/customers")

    // Create customer
    await page.getByRole("button", { name: /新建客户/ }).click()
    await page.getByLabel(/客户名称|名称/).fill("Tab Nav Co")
    await page.getByRole("button", { name: /创建|提交|保存/ }).click()
    await expect(page.getByText(/创建成功|成功/)).toBeVisible({ timeout: 5000 })

    // Navigate to detail
    await page.getByText("Tab Nav Co").first().click()
    await expect(page).toHaveURL(/\/customers\/[0-9a-f-]+/)

    // Click through tabs
    await page.getByText("联系人").click()
    await page.getByText("跟进记录").click()
    await page.getByText("基本信息").click()

    // Verify back navigation
    await page.getByRole("button", { name: /返回列表/ }).click()
    await expect(page).toHaveURL(/\/customers$/)
  })
})
