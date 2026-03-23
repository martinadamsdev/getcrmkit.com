"""种子数据：6 个默认话术模板。

用法：
    uv run python -m scripts.seed_script_templates <tenant_id>

幂等：若该 tenant 下已存在 is_system=True 模板，则跳过。
"""

from __future__ import annotations

import asyncio
import sys
import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from app.config.settings import get_settings
from app.infra.database.models.follow_up import ScriptTemplateModel

SYSTEM_TEMPLATES = [
    {
        "scene": "first_contact",
        "title": "首次开发信 — 通用版",
        "content": (
            "您好，\n\n"
            "我是 {company_name} 的 {seller_name}，专注于 {product_category} 的生产和出口，"
            "已有多年服务海外客户的经验。\n\n"
            "我们注意到贵公司在 {platform} 上对相关产品有采购需求，特此联系。"
            "我们的核心优势包括：工厂直供、支持 OEM/ODM 定制、MOQ 灵活、交期稳定。\n\n"
            "附件为我们最新的产品目录和报价单，如有兴趣请随时回复，期待合作！\n\n"
            "Best regards,\n{seller_name}"
        ),
        "position": 1,
    },
    {
        "scene": "follow_up",
        "title": "跟进回访 — 报价后 7 天",
        "content": (
            "您好 {customer_name}，\n\n"
            "上周我们发送了关于 {product_name} 的报价单，不知您是否已经查阅？\n\n"
            "如果您对价格、规格或交货期有任何疑问，我非常乐意为您进一步说明。"
            "同时，我们近期有部分现货库存，如果您有紧急需求可以优先安排发货。\n\n"
            "期待您的回复，祝商祺！\n\n"
            "Best regards,\n{seller_name}"
        ),
        "position": 2,
    },
    {
        "scene": "quotation",
        "title": "报价确认 — 附件版",
        "content": (
            "Dear {customer_name},\n\n"
            "感谢您对 {product_name} 的询价。根据您的需求，我们为您准备了详细的报价方案：\n\n"
            "- 产品型号：{model}\n"
            "- FOB 价格：USD {price}/pc\n"
            "- MOQ：{moq} pcs\n"
            "- 交货期：收到订金后 {lead_time} 天\n"
            "- 付款方式：30% T/T 预付，70% 发货前付清\n\n"
            "详细报价单请见附件 PI。如果数量较大，我们可以进一步商讨优惠价格。\n\n"
            "Best regards,\n{seller_name}"
        ),
        "position": 3,
    },
    {
        "scene": "sample",
        "title": "样品跟进 — 物流确认",
        "content": (
            "您好 {customer_name}，\n\n"
            "您订购的样品已经通过 {courier}（快递单号：{tracking_no}）寄出，"
            "预计 {eta} 到达。请注意查收。\n\n"
            "收到样品后，如果对质量、颜色、尺寸等方面有任何意见或需要调整的地方，"
            "请随时告知我们，我们将尽快配合修改。\n\n"
            "期待您的反馈！\n\n"
            "Best regards,\n{seller_name}"
        ),
        "position": 4,
    },
    {
        "scene": "order_confirm",
        "title": "订单确认 — PI 已发",
        "content": (
            "Dear {customer_name},\n\n"
            "感谢您的订单！我们已根据沟通确认的内容为您生成了 Proforma Invoice（PI），"
            "请查看附件。\n\n"
            "请您核实以下关键信息：\n"
            "- 产品规格及数量\n"
            "- 单价及总金额\n"
            "- 交货方式及港口\n"
            "- 付款方式\n\n"
            "确认无误后，请签回 PI 并安排预付款。收到订金后，我们将立即安排生产，"
            "预计交货期为 {lead_time} 天。\n\n"
            "Best regards,\n{seller_name}"
        ),
        "position": 5,
    },
    {
        "scene": "after_sales",
        "title": "售后关怀 — 到货回访",
        "content": (
            "您好 {customer_name}，\n\n"
            "根据物流信息，您的货物应该已经到达。想跟您确认一下收货情况：\n\n"
            "1. 货物是否完好无损？\n"
            "2. 数量和规格是否与订单一致？\n"
            "3. 产品质量是否满意？\n\n"
            "如有任何问题，请第一时间联系我们，我们会尽快协助处理。"
            "同时，如果后续有新的采购计划，欢迎随时联系，我们会为老客户提供更优惠的价格。\n\n"
            "感谢您的信任与支持！\n\n"
            "Best regards,\n{seller_name}"
        ),
        "position": 6,
    },
]


async def seed_system_templates(tenant_id: uuid.UUID, db_url: str | None = None) -> int:
    """为指定 tenant 插入 6 个系统话术模板。返回插入数量。

    幂等：若已存在 is_system=True 模板，跳过不重复插入。
    """
    if db_url is None:
        db_url = get_settings().database_url

    engine = create_async_engine(db_url, poolclass=NullPool)
    async with engine.begin() as conn:
        session = AsyncSession(bind=conn, expire_on_commit=False)

        # 检查是否已存在系统模板
        count_stmt = (
            select(func.count())
            .select_from(ScriptTemplateModel)
            .where(
                ScriptTemplateModel.tenant_id == tenant_id,
                ScriptTemplateModel.is_system.is_(True),
            )
        )
        existing_count = (await session.execute(count_stmt)).scalar_one()

        if existing_count >= len(SYSTEM_TEMPLATES):
            print(f"已存在 {existing_count} 个系统模板，跳过。")
            await engine.dispose()
            return 0

        now = datetime.now(UTC)
        inserted = 0
        for tpl in SYSTEM_TEMPLATES:
            # 检查该 scene 是否已存在系统模板
            exists_stmt = (
                select(func.count())
                .select_from(ScriptTemplateModel)
                .where(
                    ScriptTemplateModel.tenant_id == tenant_id,
                    ScriptTemplateModel.scene == tpl["scene"],
                    ScriptTemplateModel.is_system.is_(True),
                )
            )
            exists = (await session.execute(exists_stmt)).scalar_one()
            if exists > 0:
                continue

            model = ScriptTemplateModel(
                id=uuid.uuid7(),
                tenant_id=tenant_id,
                scene=tpl["scene"],
                title=tpl["title"],
                content=tpl["content"],
                language="zh-CN",
                position=tpl["position"],
                is_system=True,
                created_by=None,
                created_at=now,
                updated_at=now,
            )
            session.add(model)
            inserted += 1

        # conn.begin() auto-commits on exit
        print(f"成功插入 {inserted} 个系统话术模板（tenant: {tenant_id}）")

    await engine.dispose()
    return inserted


async def main() -> None:
    if len(sys.argv) < 2:
        print("用法: uv run python -m scripts.seed_script_templates <tenant_id>")
        sys.exit(1)

    tenant_id = uuid.UUID(sys.argv[1])
    await seed_system_templates(tenant_id)


if __name__ == "__main__":
    asyncio.run(main())
