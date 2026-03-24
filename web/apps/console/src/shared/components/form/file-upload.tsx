import { useState } from "react"
import { useDropzone } from "react-dropzone"
import { Upload, X, FileIcon } from "lucide-react"
import { Button } from "@workspace/ui/components/button"

type FileUploadProps = {
  accept?: Record<string, string[]>
  maxSize?: number
  onUpload: (file: File) => void
  multiple?: boolean
  className?: string
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

export function FileUpload({
  accept,
  maxSize,
  onUpload,
  multiple = false,
  className,
}: FileUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept,
    maxSize,
    multiple,
    onDrop: (acceptedFiles) => {
      setError(null)
      if (acceptedFiles.length > 0) {
        const file = acceptedFiles[0]
        setSelectedFile(file)
        onUpload(file)
      }
    },
    onDropRejected: (rejections) => {
      const rejection = rejections[0]
      if (rejection?.errors[0]?.code === "file-too-large") {
        setError(
          `File too large. Maximum size: ${maxSize ? formatFileSize(maxSize) : "unknown"}`,
        )
      } else {
        setError(rejection?.errors[0]?.message ?? "File rejected")
      }
    },
  })

  const removeFile = () => {
    setSelectedFile(null)
    setError(null)
  }

  return (
    <div className={className}>
      {!selectedFile ? (
        <div
          {...getRootProps()}
          className={`flex cursor-pointer flex-col items-center justify-center gap-2 rounded-lg border-2 border-dashed p-8 transition-colors ${
            isDragActive
              ? "border-primary bg-primary/5"
              : "border-muted-foreground/25 hover:border-muted-foreground/50"
          }`}
        >
          <input {...getInputProps()} />
          <Upload className="size-8 text-muted-foreground" />
          <p className="text-sm text-muted-foreground">
            Click or drag file to upload
          </p>
        </div>
      ) : (
        <div className="flex items-center gap-3 rounded-lg border p-3">
          <FileIcon className="size-8 text-muted-foreground" />
          <div className="flex-1 min-w-0">
            <p className="truncate text-sm font-medium">{selectedFile.name}</p>
            <p className="text-xs text-muted-foreground">
              {formatFileSize(selectedFile.size)}
            </p>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={removeFile}
            aria-label="Remove file"
          >
            <X className="size-4" />
          </Button>
        </div>
      )}
      {error && (
        <p className="mt-2 text-sm text-destructive">{error}</p>
      )}
    </div>
  )
}
