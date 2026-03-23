from enum import StrEnum


class FollowUpMethod(StrEnum):
    """跟进方式"""

    PHONE = "phone"
    EMAIL = "email"
    WECHAT = "wechat"
    WHATSAPP = "whatsapp"
    ALIBABA = "alibaba"
    MEETING = "meeting"
    EXHIBITION = "exhibition"
    OTHER = "other"


class ScriptScene(StrEnum):
    """话术场景"""

    FIRST_CONTACT = "first_contact"
    FOLLOW_UP = "follow_up"
    QUOTATION = "quotation"
    SAMPLE = "sample"
    ORDER_CONFIRM = "order_confirm"
    AFTER_SALES = "after_sales"
    REACTIVATION = "reactivation"
