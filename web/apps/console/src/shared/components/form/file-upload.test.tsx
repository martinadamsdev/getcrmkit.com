import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, it, expect, vi } from "vitest"
import { FileUpload } from "./file-upload"

function createFile(name: string, size: number, type: string) {
  const buffer = new ArrayBuffer(size)
  return new File([buffer], name, { type })
}

describe("FileUpload", () => {
  it("renders dropzone area with upload icon and text", () => {
    render(<FileUpload onUpload={vi.fn()} />)
    expect(screen.getByText(/drag|drop|click|upload/i)).toBeInTheDocument()
  })

  it("calls onUpload with file when file selected via input", async () => {
    const user = userEvent.setup()
    const onUpload = vi.fn()
    render(<FileUpload onUpload={onUpload} />)
    const input = document.querySelector('input[type="file"]') as HTMLInputElement
    const file = createFile("test.xlsx", 1024, "application/vnd.ms-excel")
    await user.upload(input, file)
    expect(onUpload).toHaveBeenCalledWith(file)
  })

  it("shows file name and size after file selected", async () => {
    const user = userEvent.setup()
    render(<FileUpload onUpload={vi.fn()} />)
    const input = document.querySelector('input[type="file"]') as HTMLInputElement
    const file = createFile("report.xlsx", 2048, "application/vnd.ms-excel")
    await user.upload(input, file)
    expect(screen.getByText("report.xlsx")).toBeInTheDocument()
  })

  it("rejects files exceeding maxSize", async () => {
    const user = userEvent.setup()
    const onUpload = vi.fn()
    render(<FileUpload onUpload={onUpload} maxSize={100} />)
    const input = document.querySelector('input[type="file"]') as HTMLInputElement
    const file = createFile("big.xlsx", 200, "application/vnd.ms-excel")
    await user.upload(input, file)
    // onUpload should not be called for oversized file
    expect(onUpload).not.toHaveBeenCalled()
    expect(screen.getByText(/too large|exceeds/i)).toBeInTheDocument()
  })
})
