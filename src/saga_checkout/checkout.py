from saga_checkout.models import CheckoutResult, Order
from saga_checkout.saga import CheckoutSaga, SagaStep
from saga_checkout.services import InventoryService, PaymentService, ShippingService


class CheckoutService:
    def __init__(
        self,
        payment_service: PaymentService,
        inventory_service: InventoryService,
        shipping_service: ShippingService,
    ) -> None:
        self.payment_service = payment_service
        self.inventory_service = inventory_service
        self.shipping_service = shipping_service

        self.saga = CheckoutSaga(
            steps=[
                SagaStep(
                    name="payment",
                    do_action=self.payment_service.do,
                    compensate_action=self.payment_service.compensate,
                ),
                SagaStep(
                    name="inventory",
                    do_action=self.inventory_service.do,
                    compensate_action=self.inventory_service.compensate,
                ),
                SagaStep(
                    name="shipping",
                    do_action=self.shipping_service.do,
                    compensate_action=self.shipping_service.compensate,
                ),
            ]
        )

    def checkout(self, order: Order) -> CheckoutResult:
        return self.saga.execute(order)
