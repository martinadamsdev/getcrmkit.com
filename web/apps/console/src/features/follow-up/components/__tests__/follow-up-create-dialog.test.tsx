import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { FollowUpCreateDialog } from "../follow-up-create-dialog";

function wrapper({ children }: { children: React.ReactNode }) {
  const qc = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return <QueryClientProvider client={qc}>{children}</QueryClientProvider>;
}

describe("FollowUpCreateDialog", () => {
  it("renders dialog title when open", () => {
    render(
      <FollowUpCreateDialog open onOpenChange={() => {}} />,
      { wrapper },
    );
    expect(screen.getByText("新建跟进记录")).toBeInTheDocument();
  });

  it("renders method select with label", () => {
    render(
      <FollowUpCreateDialog open onOpenChange={() => {}} />,
      { wrapper },
    );
    expect(screen.getByText("跟进方式")).toBeInTheDocument();
  });

  it("renders content textarea", () => {
    render(
      <FollowUpCreateDialog open onOpenChange={() => {}} />,
      { wrapper },
    );
    expect(
      screen.getByPlaceholderText("跟进内容..."),
    ).toBeInTheDocument();
  });

  it("renders customer response field", () => {
    render(
      <FollowUpCreateDialog open onOpenChange={() => {}} />,
      { wrapper },
    );
    expect(
      screen.getByPlaceholderText("客户反馈..."),
    ).toBeInTheDocument();
  });

  it("renders submit button", () => {
    render(
      <FollowUpCreateDialog open onOpenChange={() => {}} />,
      { wrapper },
    );
    expect(
      screen.getByRole("button", { name: /保存/ }),
    ).toBeInTheDocument();
  });

  it("does not render when closed", () => {
    render(
      <FollowUpCreateDialog open={false} onOpenChange={() => {}} />,
      { wrapper },
    );
    expect(screen.queryByText("新建跟进记录")).not.toBeInTheDocument();
  });
});
