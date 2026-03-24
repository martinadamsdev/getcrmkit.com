import { test, expect } from "@playwright/test"

// 唯一邮箱生成，避免测试间冲突
const uniqueEmail = () => `e2e-${Date.now()}-${Math.random().toString(36).slice(2, 8)}@test.com`

test.describe("Authentication", () => {
  test("should show login page by default", async ({ page }) => {
    await page.goto("/")
    await expect(page).toHaveURL(/\/login/)
    await expect(page.getByRole("heading", { name: /登录/i })).toBeVisible()
  })

  test("should show register page", async ({ page }) => {
    await page.goto("/register")
    await expect(page.getByRole("heading", { name: /注册/i })).toBeVisible()
  })

  test("should navigate between login and register", async ({ page }) => {
    await page.goto("/login")
    await page.getByRole("link", { name: /注册/i }).click()
    await expect(page).toHaveURL(/\/register/)

    await page.getByRole("link", { name: /登录/i }).click()
    await expect(page).toHaveURL(/\/login/)
  })

  test("should register a new user", async ({ page }) => {
    const email = uniqueEmail()
    await page.goto("/register")

    await page.getByLabel(/姓名/i).fill("E2E User")
    await page.getByLabel(/邮箱/i).fill(email)
    await page.getByLabel(/^密码$/i).fill("TestPass123")
    await page.getByLabel(/确认密码/i).fill("TestPass123")
    await page.getByRole("button", { name: /注册/i }).click()

    // 注册成功后应跳转到登录页
    await expect(page).toHaveURL(/\/login/, { timeout: 5000 })
  })

  test("should show error for duplicate email registration", async ({ page }) => {
    const email = uniqueEmail()

    // 先注册
    await page.goto("/register")
    await page.getByLabel(/姓名/i).fill("First User")
    await page.getByLabel(/邮箱/i).fill(email)
    await page.getByLabel(/^密码$/i).fill("TestPass123")
    await page.getByLabel(/确认密码/i).fill("TestPass123")
    await page.getByRole("button", { name: /注册/i }).click()
    await expect(page).toHaveURL(/\/login/, { timeout: 5000 })

    // 再用同邮箱注册
    await page.goto("/register")
    await page.getByLabel(/姓名/i).fill("Second User")
    await page.getByLabel(/邮箱/i).fill(email)
    await page.getByLabel(/^密码$/i).fill("TestPass123")
    await page.getByLabel(/确认密码/i).fill("TestPass123")
    await page.getByRole("button", { name: /注册/i }).click()

    await expect(page.getByText(/已注册/i)).toBeVisible({ timeout: 5000 })
  })

  test("should login successfully", async ({ page }) => {
    const email = uniqueEmail()

    // 先注册
    await page.goto("/register")
    await page.getByLabel(/姓名/i).fill("Login Test")
    await page.getByLabel(/邮箱/i).fill(email)
    await page.getByLabel(/^密码$/i).fill("TestPass123")
    await page.getByLabel(/确认密码/i).fill("TestPass123")
    await page.getByRole("button", { name: /注册/i }).click()
    await expect(page).toHaveURL(/\/login/, { timeout: 5000 })

    // 登录
    await page.getByLabel(/邮箱/i).fill(email)
    await page.getByLabel(/密码/i).fill("TestPass123")
    await page.getByRole("button", { name: /登录/i }).click()

    // 登录成功应离开 /login
    await expect(page).not.toHaveURL(/\/login/, { timeout: 5000 })
  })

  test("should show error for wrong password", async ({ page }) => {
    const email = uniqueEmail()

    // 先注册
    await page.goto("/register")
    await page.getByLabel(/姓名/i).fill("Wrong PW User")
    await page.getByLabel(/邮箱/i).fill(email)
    await page.getByLabel(/^密码$/i).fill("TestPass123")
    await page.getByLabel(/确认密码/i).fill("TestPass123")
    await page.getByRole("button", { name: /注册/i }).click()
    await expect(page).toHaveURL(/\/login/, { timeout: 5000 })

    // 用错密码登录
    await page.getByLabel(/邮箱/i).fill(email)
    await page.getByLabel(/密码/i).fill("WrongPassword99")
    await page.getByRole("button", { name: /登录/i }).click()

    await expect(page.getByText(/失败|错误/i)).toBeVisible({ timeout: 5000 })
  })

  test("should redirect unauthenticated user to login", async ({ page }) => {
    await page.goto("/")
    await expect(page).toHaveURL(/\/login/)
  })

  test("should redirect authenticated user from login to home", async ({ page }) => {
    const email = uniqueEmail()

    // 注册 + 登录
    await page.goto("/register")
    await page.getByLabel(/姓名/i).fill("Redirect User")
    await page.getByLabel(/邮箱/i).fill(email)
    await page.getByLabel(/^密码$/i).fill("TestPass123")
    await page.getByLabel(/确认密码/i).fill("TestPass123")
    await page.getByRole("button", { name: /注册/i }).click()
    await expect(page).toHaveURL(/\/login/, { timeout: 5000 })

    await page.getByLabel(/邮箱/i).fill(email)
    await page.getByLabel(/密码/i).fill("TestPass123")
    await page.getByRole("button", { name: /登录/i }).click()
    await expect(page).not.toHaveURL(/\/login/, { timeout: 5000 })

    // 再访问 /login 应被重定向
    await page.goto("/login")
    await expect(page).not.toHaveURL(/\/login/, { timeout: 5000 })
  })

  test("should show password strength indicator on register", async ({ page }) => {
    await page.goto("/register")

    await page.getByLabel(/^密码$/i).fill("ab")
    await expect(page.getByText(/弱/i)).toBeVisible()

    await page.getByLabel(/^密码$/i).fill("password1")
    await expect(page.getByText(/中/i)).toBeVisible()

    await page.getByLabel(/^密码$/i).fill("P@ssw0rd123!")
    await expect(page.getByText(/强/i)).toBeVisible()
  })
})
