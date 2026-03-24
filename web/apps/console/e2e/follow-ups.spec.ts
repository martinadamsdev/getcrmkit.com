import { expect, test } from "@playwright/test";

test.describe("Follow-Up Records Page", () => {
  test.beforeEach(async ({ page }) => {
    // Assumes auth is handled by test setup (login fixture)
    await page.goto("/follow-ups");
  });

  test("renders split layout with table and template panel", async ({
    page,
  }) => {
    await expect(page.getByText("跟进记录")).toBeVisible();
    await expect(page.getByText("话术模板")).toBeVisible();
  });

  test("renders all 7 script scene headings in panel", async ({
    page,
  }) => {
    const scenes = [
      "首次联系",
      "跟进回复",
      "报价跟进",
      "样品跟进",
      "订单确认",
      "售后跟进",
      "客户激活",
    ];
    for (const scene of scenes) {
      await expect(page.getByText(scene)).toBeVisible();
    }
  });

  test("opens create dialog and shows form fields", async ({ page }) => {
    await page.getByRole("button", { name: /新建跟进/ }).click();
    await expect(page.getByText("新建跟进记录")).toBeVisible();
    await expect(page.getByText("跟进方式")).toBeVisible();
    await expect(page.getByPlaceholder("跟进内容...")).toBeVisible();
    await expect(page.getByPlaceholder("客户反馈...")).toBeVisible();
  });

  test("create follow-up flow", async ({ page }) => {
    await page.getByRole("button", { name: /新建跟进/ }).click();

    // Fill content
    await page
      .getByPlaceholder("跟进内容...")
      .fill("Test follow-up content from E2E");
    await page
      .getByPlaceholder("客户反馈...")
      .fill("Customer is interested");

    // Note: Full creation test requires CustomerPicker + auth + backend running
    // This test verifies the form UI works
    await expect(
      page.getByRole("button", { name: /保存/ }),
    ).toBeVisible();
  });

  test("copy script template to clipboard", async ({ page, context }) => {
    // Grant clipboard permission
    await context.grantPermissions([
      "clipboard-read",
      "clipboard-write",
    ]);

    // Find a copy button in the template panel (if templates exist)
    const copyButtons = page.getByRole("button", { name: /复制/ });
    const count = await copyButtons.count();
    if (count > 0) {
      await copyButtons.first().click();
      // Verify toast appears
      await expect(page.getByText("已复制到剪贴板")).toBeVisible();
    }
  });

  test("toggle filters panel", async ({ page }) => {
    await page.getByRole("button", { name: /筛选/ }).click();
    await expect(page.getByText("全部方式")).toBeVisible();
  });

  test("report period toggle works", async ({ page }) => {
    await expect(page.getByText("日报")).toBeVisible();
    await page.getByText("周报").click();
    // Toggle should update
    await expect(page.getByText("周报")).toBeVisible();
  });

  test("export button is clickable", async ({ page }) => {
    const exportBtn = page.getByRole("button", { name: /导出/ });
    await expect(exportBtn).toBeVisible();
    await expect(exportBtn).toBeEnabled();
  });
});
