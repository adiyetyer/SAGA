from dataclasses import dataclass
from typing import Callable, List

from saga_checkout.models import CheckoutResult, Order


@dataclass
class SagaStep:
    name: str
    do_action: Callable[[Order], None]
    compensate_action: Callable[[Order], None]


class CheckoutSaga:
    def __init__(self, steps: List[SagaStep]) -> None:
        self.steps = steps

    def execute(self, order: Order) -> CheckoutResult:
        completed_steps: List[SagaStep] = []
        compensated_step_names: List[str] = []

        try:
            for step in self.steps:
                step.do_action(order)
                completed_steps.append(step)

            return CheckoutResult(
                success=True,
                message="Checkout completed successfully",
                completed_steps=[step.name for step in completed_steps],
                compensated_steps=[],
            )
        except Exception as exc:
            for step in reversed(completed_steps):
                step.compensate_action(order)
                compensated_step_names.append(step.name)

            return CheckoutResult(
                success=False,
                message=f"Checkout failed: {exc}",
                completed_steps=[step.name for step in completed_steps],
                compensated_steps=compensated_step_names,
            )
