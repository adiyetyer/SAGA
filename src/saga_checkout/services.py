from saga_checkout.models import Order


class PaymentService:
    def __init__(self) -> None:
        self.charged_orders: set[str] = set()
        self.refunded_orders: set[str] = set()

    def do(self, order: Order) -> None:
        self.charged_orders.add(order.order_id)

    def compensate(self, order: Order) -> None:
        if order.order_id in self.charged_orders:
            self.charged_orders.remove(order.order_id)
            self.refunded_orders.add(order.order_id)


class InventoryService:
    def __init__(self, stock: dict[str, int]) -> None:
        self.stock = stock
        self.reserved: dict[str, int] = {}

    def do(self, order: Order) -> None:
        available = self.stock.get(order.item_sku, 0)
        if available < order.quantity:
            raise ValueError("Not enough inventory")

        self.stock[order.item_sku] = available - order.quantity
        self.reserved[order.order_id] = order.quantity

    def compensate(self, order: Order) -> None:
        quantity = self.reserved.pop(order.order_id, 0)
        self.stock[order.item_sku] = self.stock.get(order.item_sku, 0) + quantity


class ShippingService:
    def __init__(self) -> None:
        self.created_shipments: set[str] = set()
        self.cancelled_shipments: set[str] = set()

    def do(self, order: Order) -> None:
        if not order.address.strip():
            raise ValueError("Shipping address is required")

        self.created_shipments.add(order.order_id)

    def compensate(self, order: Order) -> None:
        if order.order_id in self.created_shipments:
            self.created_shipments.remove(order.order_id)
            self.cancelled_shipments.add(order.order_id)
