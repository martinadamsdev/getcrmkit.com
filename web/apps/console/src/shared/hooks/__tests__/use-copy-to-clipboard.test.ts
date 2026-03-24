import { act, renderHook } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { useCopyToClipboard } from "../use-copy-to-clipboard";

describe("useCopyToClipboard", () => {
  beforeEach(() => {
    Object.assign(navigator, {
      clipboard: {
        writeText: vi.fn().mockResolvedValue(undefined),
      },
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("initial state: copied is false", () => {
    const { result } = renderHook(() => useCopyToClipboard());
    expect(result.current.copied).toBe(false);
  });

  it("copy sets copied to true and returns true", async () => {
    const { result } = renderHook(() => useCopyToClipboard());
    let success: boolean | undefined;
    await act(async () => {
      success = await result.current.copy("hello");
    });
    expect(success).toBe(true);
    expect(result.current.copied).toBe(true);
    expect(navigator.clipboard.writeText).toHaveBeenCalledWith("hello");
  });

  it("copied resets to false after timeout", async () => {
    vi.useFakeTimers();
    const { result } = renderHook(() => useCopyToClipboard(1000));
    await act(async () => {
      await result.current.copy("text");
    });
    expect(result.current.copied).toBe(true);
    act(() => {
      vi.advanceTimersByTime(1000);
    });
    expect(result.current.copied).toBe(false);
    vi.useRealTimers();
  });

  it("handles clipboard error gracefully and returns false", async () => {
    (
      navigator.clipboard.writeText as ReturnType<typeof vi.fn>
    ).mockRejectedValueOnce(new Error("denied"));
    const { result } = renderHook(() => useCopyToClipboard());
    let success: boolean | undefined;
    await act(async () => {
      success = await result.current.copy("text");
    });
    expect(success).toBe(false);
    expect(result.current.copied).toBe(false);
  });
});
