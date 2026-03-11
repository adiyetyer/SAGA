from saga_checkout.checkout import CheckoutService
from saga_checkout.models import Order
from saga_checkout.services import InventoryService, PaymentService, ShippingService


def run_demo() -> None:
    payment = PaymentService()
    inventory = InventoryService(stock={"laptop": 5})
    shipping = ShippingService()
    checkout = CheckoutService(payment, inventory, shipping)

    success_order = Order(
        order_id="order-1",
        amount=1299.99,
        item_sku="laptop",
        quantity=1,
        address="Almaty, Kazakhstan",
    )
    failed_order = Order(
        order_id="order-2",
        amount=1299.99,
        item_sku="laptop",
        quantity=10,
        address="Almaty, Kazakhstan",
    )

    print("SUCCESS CASE")
    print(checkout.checkout(success_order))
    print()
    print("FAILURE CASE WITH COMPENSATION")
    print(checkout.checkout(failed_order))


if __name__ == "__main__":
    run_demo()
