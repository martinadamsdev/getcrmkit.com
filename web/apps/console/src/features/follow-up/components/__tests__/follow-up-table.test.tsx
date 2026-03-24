import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { FollowUpTable } from "../follow-up-table";

const MOCK_DATA = [
  {
    id: "fu-1",
    customer_id: "cust-1",
    customer_name: "Acme Corp",
    contact_id: null,
    method: "email",
    stage: "contacted",
    content:
      "Sent initial product catalog and pricing information to the buyer",
    customer_response: "Interested in MOQ",
    next_follow_at: "2026-03-25T09:00:00Z",
    attachment_urls: [],
    tags: ["重点客户", "报价中"],
    created_by: "user-1",
    created_at: "2026-03-20T14:30:00Z",
    updated_at: "2026-03-20T14:30:00Z",
  },
];

describe("FollowUpTable", () => {
  it("renders table headers", () => {
    render(
      <FollowUpTable
        data={MOCK_DATA}
        total={1}
        page={1}
        pageSize={20}
        onPageChange={() => {}}
      />,
    );
    expect(screen.getByText("客户")).toBeInTheDocument();
    expect(screen.getByText("方式")).toBeInTheDocument();
    expect(screen.getByText("内容")).toBeInTheDocument();
    expect(screen.getByText("标签")).toBeInTheDocument();
    expect(screen.getByText("时间")).toBeInTheDocument();
    expect(screen.getByText("下次跟进")).toBeInTheDocument();
  });

  it("renders follow-up row data", () => {
    render(
      <FollowUpTable
        data={MOCK_DATA}
        total={1}
        page={1}
        pageSize={20}
        onPageChange={() => {}}
      />,
    );
    expect(screen.getByText("Acme Corp")).toBeInTheDocument();
    expect(
      screen.getByText(/Sent initial product catalog/),
    ).toBeInTheDocument();
  });

  it("renders tags as badges", () => {
    render(
      <FollowUpTable
        data={MOCK_DATA}
        total={1}
        page={1}
        pageSize={20}
        onPageChange={() => {}}
      />,
    );
    expect(screen.getByText("重点客户")).toBeInTheDocument();
    expect(screen.getByText("报价中")).toBeInTheDocument();
  });

  it("renders method icon", () => {
    render(
      <FollowUpTable
        data={MOCK_DATA}
        total={1}
        page={1}
        pageSize={20}
        onPageChange={() => {}}
      />,
    );
    expect(screen.getByLabelText("邮件")).toBeInTheDocument();
  });

  it("renders empty state when no data", () => {
    render(
      <FollowUpTable
        data={[]}
        total={0}
        page={1}
        pageSize={20}
        onPageChange={() => {}}
      />,
    );
    expect(screen.getByText(/暂无跟进记录/)).toBeInTheDocument();
  });
});
