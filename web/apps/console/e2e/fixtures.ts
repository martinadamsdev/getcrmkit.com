import { test as base } from "@playwright/test"

// Auth fixture: registers + logs in before each test
export const test = base.extend({
  page: async ({ page }, use) => {
    const email = `e2e-${Date.now()}-${Math.random().toString(36).slice(2, 8)}@test.com`

    // Register
    await page.goto("/register")
    await page.getByLabel(/姓名/i).fill("E2E Customer User")
    await page.getByLabel(/邮箱/i).fill(email)
    await page.getByLabel(/^密码$/i).fill("TestPass123")
    await page.getByLabel(/确认密码/i).fill("TestPass123")
    await page.getByRole("button", { name: /注册/i }).click()
    await page.waitForURL(/\/login/, { timeout: 5000 })

    // Login
    await page.getByLabel(/邮箱/i).fill(email)
    await page.getByLabel(/密码/i).fill("TestPass123")
    await page.getByRole("button", { name: /登录/i }).click()
    await page.waitForURL(/^(?!.*\/login)/, { timeout: 5000 })

    await use(page)
  },
})

export { expect } from "@playwright/test"
