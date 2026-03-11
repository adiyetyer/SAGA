import unittest

from saga_checkout import CheckoutService, InventoryService, Order, PaymentService, ShippingService


class CheckoutSagaTests(unittest.TestCase):
    def test_checkout_success(self) -> None:
        payment = PaymentService()
        inventory = InventoryService(stock={"book": 3})
        shipping = ShippingService()
        checkout = CheckoutService(payment, inventory, shipping)

        result = checkout.checkout(
            Order(
                order_id="ok-1",
                amount=20.0,
                item_sku="book",
                quantity=1,
                address="Astana",
            )
        )

        self.assertTrue(result.success)
        self.assertEqual(result.completed_steps, ["payment", "inventory", "shipping"])
        self.assertEqual(result.compensated_steps, [])
        self.assertIn("ok-1", payment.charged_orders)
        self.assertEqual(inventory.stock["book"], 2)
        self.assertIn("ok-1", shipping.created_shipments)

    def test_checkout_failure_compensates_in_reverse(self) -> None:
        payment = PaymentService()
        inventory = InventoryService(stock={"book": 1})
        shipping = ShippingService()
        checkout = CheckoutService(payment, inventory, shipping)

        result = checkout.checkout(
            Order(
                order_id="fail-1",
                amount=20.0,
                item_sku="book",
                quantity=2,
                address="Astana",
            )
        )

        self.assertFalse(result.success)
        self.assertEqual(result.completed_steps, ["payment"])
        self.assertEqual(result.compensated_steps, ["payment"])
        self.assertNotIn("fail-1", payment.charged_orders)
        self.assertIn("fail-1", payment.refunded_orders)
        self.assertEqual(inventory.stock["book"], 1)
        self.assertNotIn("fail-1", shipping.created_shipments)


if __name__ == "__main__":
    unittest.main()
