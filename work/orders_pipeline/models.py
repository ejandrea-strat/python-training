"""Defines OrderRecord, the object that holds one valid order."""

from orders_pipeline.validators import safe_to_float


class OrderRecord:
    count = 0

    def __init__(self, order_id, product, quantity, unit_price):
        self.order_id = order_id
        self.product = product

        # quantity has to be a whole number
        try:
            self.quantity = int(quantity)
        except ValueError as err:
            raise ValueError(f"quantity {quantity!r} is not a whole number") from err

        # reject policy: quantity must be above 0
        if self.quantity <= 0:
            raise ValueError(f"quantity must be above 0, got {self.quantity}")

        self.unit_price = safe_to_float(unit_price)
        OrderRecord.count += 1

    def total(self):
        return self.quantity * self.unit_price

    def __repr__(self):
        return (f"OrderRecord(order_id={self.order_id!r}, product={self.product!r}, "
                f"quantity={self.quantity!r}, unit_price={self.unit_price!r})")