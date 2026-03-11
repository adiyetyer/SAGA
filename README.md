# Simple Checkout Saga

This project implements a lightweight Saga Pattern inside a single microservice for an e-commerce checkout flow.

## Workflow

The checkout runs three steps in order:

1. `Payment`
2. `Inventory`
3. `Shipping`

Each step exposes:

- a `do` action to apply the step
- a `compensate` action to undo the step

If any step fails, the service compensates already completed steps in reverse order.

## Design

The implementation keeps everything intentionally simple:

- `PaymentService` simulates charging and refunding
- `InventoryService` simulates reserving and restoring stock
- `ShippingService` simulates creating and cancelling shipments
- `CheckoutSaga` is the orchestrator
- `CheckoutService` wires the checkout steps together

This demonstrates the core Saga idea without extra infrastructure such as queues, brokers, or separate processes.

## Project Structure

```text
src/saga_checkout/
  checkout.py
  demo.py
  models.py
  saga.py
  services.py
tests/
  test_checkout_saga.py
```

## Run the demo

```bash
cd saga-checkout-demo
PYTHONPATH=src python3 -m saga_checkout.demo
```

## Run the tests

```bash
cd saga-checkout-demo
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Example behavior

- success path: payment, inventory, and shipping all complete
- failure path: if inventory or shipping fails, earlier successful steps are compensated automatically

## Repository link

Target repository for publishing:

- [adiyetyer/SAGA](https://github.com/adiyetyer/SAGA.git)
