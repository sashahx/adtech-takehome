from unittest.mock import Mock, patch

from expects import equal, expect
from mamba import after, before, description, it

from app import app
from src.adapters.database_adapters import DatabaseAdapter


class MockOrderForm(Mock):
    name = type("DataAttributeHolder", (), {"data": "John Doe"})
    address = type("DataAttributeHolder", (), {"data": "idk some address"})

    @staticmethod
    def validate() -> bool:
        return True


with description("create order endpoint") as self:
    with before.all:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///spec_db"
        self.client = app.test_client()

    with after.all:
        DatabaseAdapter(app.config["SQLALCHEMY_DATABASE_URI"]).clear_table()

    with it("tries to create an order and should fail"):
        response = self.client.post("/create", data={})
        expect(response.status_code).to(equal(400))

    with it("tries to create an order and should succeed"):
        with patch("app.OrderForm", MockOrderForm, create=True):
            response = self.client.post("/create")
        expect(response.status_code).to(equal(200))

    with it("tries to get an order created at previous step"):
        order = DatabaseAdapter(app.config["SQLALCHEMY_DATABASE_URI"]).get_order(1)
        expect(order.get("name")).to(equal(MockOrderForm.name.data))  # type: ignore
        expect(order.get("address")).to(equal(MockOrderForm.address.data))  # type: ignore
