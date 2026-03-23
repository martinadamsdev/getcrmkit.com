from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "CNY"

    def __post_init__(self) -> None:
        if self.amount < 0:
            msg = "Amount cannot be negative"
            raise ValueError(msg)
