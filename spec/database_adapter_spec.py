from datetime import datetime

from expects import equal, expect
from mamba import after, before, description, it

from src.adapters.database_adapters import DatabaseAdapter
from src.domain.order import Order

with description("database") as self:
    with before.all:
        self.database = DatabaseAdapter("sqlite:///spec_db")
        self.order_attributes = {
            "id": 0,
            "name": "John",
            "address": "Doe",
            "created_at": datetime(2023, 12, 6),
            "updated_at": datetime(2023, 12, 6),
        }

    with after.all:
        self.database.clear_table()

    with it("receives a new order to insert"):
        order = Order(**self.order_attributes)
        self.database.create_order(order)
        expect(self.database.get_order(0)).to(equal(self.order_attributes))
