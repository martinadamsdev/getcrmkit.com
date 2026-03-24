import { describe, expect, it, vi, beforeAll, afterAll, afterEach } from "vitest"
import { screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { http, HttpResponse } from "msw"
import { renderWithProviders } from "@/test/render"
import { server } from "@/test/msw/server"
import { ImportDialog } from "./import-dialog"

const systemFields = [
  { key: "name", label: "客户名称", required: true },
  { key: "country", label: "国家" },
  { key: "email", label: "邮箱" },
  { key: "phone", label: "电话" },
  { key: "industry", label: "行业" },
]

const defaultProps = {
  open: true,
  onOpenChange: vi.fn(),
  entityType: "customer" as const,
  uploadEndpoint: "/api/v1/customers/import",
  systemFields,
  onComplete: vi.fn(),
}

beforeAll(() => server.listen({ onUnhandledRequest: "bypass" }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe("ImportDialog", () => {
  it("Step 1: renders FileUpload for xlsx/csv/xls", () => {
    renderWithProviders(<ImportDialog {...defaultProps} />)
    expect(screen.getByText(/Click or drag file to upload/)).toBeInTheDocument()
    expect(screen.getByText(/支持 .xlsx、.xls、.csv/)).toBeInTheDocument()
  })

  it("Step 1: '下一步' disabled until file uploaded", () => {
    renderWithProviders(<ImportDialog {...defaultProps} />)
    const nextBtn = screen.getByRole("button", { name: /下一步/ })
    expect(nextBtn).toBeDisabled()
  })

  it("Step 2: renders field mapping UI after file upload", async () => {
    const user = userEvent.setup()

    // Mock file parse endpoint
    server.use(
      http.post("/api/v1/files/parse-headers", () => {
        return HttpResponse.json({
          headers: ["Company Name", "Country", "Email"],
        })
      }),
    )

    renderWithProviders(<ImportDialog {...defaultProps} />)

    // Simulate file upload by creating a mock xlsx file
    const file = new File(["test"], "customers.xlsx", {
      type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    })

    const dropzone = screen.getByText(/Click or drag file to upload/).closest("div")!
    const input = dropzone.querySelector("input[type='file']") as HTMLInputElement
    await user.upload(input, file)

    // Click next
    const nextBtn = screen.getByRole("button", { name: /下一步/ })
    await waitFor(() => expect(nextBtn).toBeEnabled())
    await user.click(nextBtn)

    // Should see mapping UI
    await waitFor(() => {
      expect(screen.getByText("字段映射")).toBeInTheDocument()
    })
  })

  it("Step 2: '开始导入' triggers POST with mapping", async () => {
    const user = userEvent.setup()
    let importCalled = false

    server.use(
      http.post("/api/v1/files/parse-headers", () => {
        return HttpResponse.json({
          headers: ["Company Name", "Country"],
        })
      }),
      http.post("/api/v1/customers/import", () => {
        importCalled = true
        return HttpResponse.json({ job_id: "job-123" })
      }),
      http.get("/api/v1/data-jobs/job-123", () => {
        return HttpResponse.json({
          id: "job-123",
          status: "completed",
          total_rows: 10,
          processed_rows: 10,
          success_count: 10,
          error_count: 0,
          errors: [],
        })
      }),
    )

    renderWithProviders(<ImportDialog {...defaultProps} />)

    const file = new File(["test"], "customers.xlsx", {
      type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    })
    const dropzone = screen.getByText(/Click or drag file to upload/).closest("div")!
    const input = dropzone.querySelector("input[type='file']") as HTMLInputElement
    await user.upload(input, file)

    const nextBtn = screen.getByRole("button", { name: /下一步/ })
    await waitFor(() => expect(nextBtn).toBeEnabled())
    await user.click(nextBtn)

    await waitFor(() => {
      expect(screen.getByText("字段映射")).toBeInTheDocument()
    })

    const importBtn = screen.getByRole("button", { name: /开始导入/ })
    await user.click(importBtn)

    await waitFor(() => expect(importCalled).toBe(true))
  })

  it("Step 3: shows progress bar polling data-jobs", async () => {
    const user = userEvent.setup()
    let pollCount = 0

    server.use(
      http.post("/api/v1/files/parse-headers", () => {
        return HttpResponse.json({ headers: ["Name"] })
      }),
      http.post("/api/v1/customers/import", () => {
        return HttpResponse.json({ job_id: "job-456" })
      }),
      http.get("/api/v1/data-jobs/job-456", () => {
        pollCount++
        if (pollCount < 2) {
          return HttpResponse.json({
            id: "job-456",
            status: "processing",
            total_rows: 100,
            processed_rows: 50,
            success_count: 50,
            error_count: 0,
            errors: [],
          })
        }
        return HttpResponse.json({
          id: "job-456",
          status: "completed",
          total_rows: 100,
          processed_rows: 100,
          success_count: 100,
          error_count: 0,
          errors: [],
        })
      }),
    )

    renderWithProviders(<ImportDialog {...defaultProps} />)

    const file = new File(["test"], "test.xlsx", {
      type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    })
    const dropzone = screen.getByText(/Click or drag file to upload/).closest("div")!
    const input = dropzone.querySelector("input[type='file']") as HTMLInputElement
    await user.upload(input, file)

    await waitFor(() => screen.getByRole("button", { name: /下一步/ }))
    await user.click(screen.getByRole("button", { name: /下一步/ }))

    await waitFor(() => screen.getByText("字段映射"))
    await user.click(screen.getByRole("button", { name: /开始导入/ }))

    // Should show progress state
    await waitFor(() => {
      expect(screen.getByText(/正在导入/)).toBeInTheDocument()
    })

    // Eventually shows completed
    await waitFor(
      () => {
        expect(screen.getByText(/导入完成/)).toBeInTheDocument()
      },
      { timeout: 10000 },
    )
  })

  it("Step 3: failed state shows error list", async () => {
    const user = userEvent.setup()

    server.use(
      http.post("/api/v1/files/parse-headers", () => {
        return HttpResponse.json({ headers: ["Name"] })
      }),
      http.post("/api/v1/customers/import", () => {
        return HttpResponse.json({ job_id: "job-err" })
      }),
      http.get("/api/v1/data-jobs/job-err", () => {
        return HttpResponse.json({
          id: "job-err",
          status: "failed",
          total_rows: 10,
          processed_rows: 3,
          success_count: 1,
          error_count: 2,
          errors: [
            { row: 2, reason: "客户名称不能为空" },
            { row: 5, reason: "邮箱格式错误" },
          ],
        })
      }),
    )

    renderWithProviders(<ImportDialog {...defaultProps} />)

    const file = new File(["test"], "test.xlsx", {
      type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    })
    const dropzone = screen.getByText(/Click or drag file to upload/).closest("div")!
    const input = dropzone.querySelector("input[type='file']") as HTMLInputElement
    await user.upload(input, file)

    await waitFor(() => screen.getByRole("button", { name: /下一步/ }))
    await user.click(screen.getByRole("button", { name: /下一步/ }))

    await waitFor(() => screen.getByText("字段映射"))
    await user.click(screen.getByRole("button", { name: /开始导入/ }))

    await waitFor(() => {
      expect(screen.getByText(/导入失败/)).toBeInTheDocument()
      expect(screen.getByText(/客户名称不能为空/)).toBeInTheDocument()
      expect(screen.getByText(/邮箱格式错误/)).toBeInTheDocument()
    })
  })
})
