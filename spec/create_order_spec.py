from dataclasses import asdict
from datetime import datetime

from expects import equal, expect
from mamba import description, it

from src.domain.order import Order

with description("order class") as self:
    with it("creates an instance"):
        order_attributes = {
            "id": 1,
            "name": "John",
            "address": "Doe",
            "created_at": datetime(2023, 12, 6),
            "updated_at": datetime(2023, 12, 6),
        }
        order_as_dictionary = asdict(Order(**order_attributes))  # type: ignore[arg-type]
        expect(order_as_dictionary).to(equal(order_attributes))
