import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ScriptTemplatePanel } from "../script-template-panel";

function wrapper({ children }: { children: React.ReactNode }) {
  const qc = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return <QueryClientProvider client={qc}>{children}</QueryClientProvider>;
}

describe("ScriptTemplatePanel", () => {
  it("renders all 7 scene headings", () => {
    render(<ScriptTemplatePanel />, { wrapper });
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
      expect(screen.getByText(scene)).toBeInTheDocument();
    }
  });

  it("renders panel title", () => {
    render(<ScriptTemplatePanel />, { wrapper });
    expect(screen.getByText("话术模板")).toBeInTheDocument();
  });
});
