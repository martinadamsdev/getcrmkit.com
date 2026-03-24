import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { FollowUpMethodIcon } from "../follow-up-method-icon";

describe("FollowUpMethodIcon", () => {
  it("renders email icon with accessible label", () => {
    render(<FollowUpMethodIcon method="email" />);
    expect(screen.getByLabelText("邮件")).toBeInTheDocument();
  });

  it("renders phone icon", () => {
    render(<FollowUpMethodIcon method="phone" />);
    expect(screen.getByLabelText("电话")).toBeInTheDocument();
  });

  it("renders wechat icon", () => {
    render(<FollowUpMethodIcon method="wechat" />);
    expect(screen.getByLabelText("微信")).toBeInTheDocument();
  });

  it("renders whatsapp icon", () => {
    render(<FollowUpMethodIcon method="whatsapp" />);
    expect(screen.getByLabelText("WhatsApp")).toBeInTheDocument();
  });

  it("renders alibaba icon", () => {
    render(<FollowUpMethodIcon method="alibaba" />);
    expect(screen.getByLabelText("阿里巴巴站内信")).toBeInTheDocument();
  });

  it("renders meeting icon", () => {
    render(<FollowUpMethodIcon method="meeting" />);
    expect(screen.getByLabelText("会面")).toBeInTheDocument();
  });

  it("renders exhibition icon", () => {
    render(<FollowUpMethodIcon method="exhibition" />);
    expect(screen.getByLabelText("展会")).toBeInTheDocument();
  });

  it("renders other/fallback icon", () => {
    render(<FollowUpMethodIcon method="other" />);
    expect(screen.getByLabelText("其他")).toBeInTheDocument();
  });

  it("accepts custom className", () => {
    const { container } = render(
      <FollowUpMethodIcon method="email" className="text-red-500" />,
    );
    expect(container.firstChild).toHaveClass("text-red-500");
  });
});
