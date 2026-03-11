from dataclasses import dataclass, field
from typing import List


@dataclass
class Order:
    order_id: str
    amount: float
    item_sku: str
    quantity: int
    address: str


@dataclass
class CheckoutResult:
    success: bool
    message: str
    completed_steps: List[str] = field(default_factory=list)
    compensated_steps: List[str] = field(default_factory=list)
