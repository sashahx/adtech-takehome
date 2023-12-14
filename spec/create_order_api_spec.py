import xml.etree.ElementTree as ET
from unittest.mock import Mock, patch

from expects import equal, expect
from mamba import after, before, description, it

from app import app
from src.adapters.database_adapters import DatabaseAdapter


class MockCreateOrderForm(Mock):
    name = type("DataAttributeHolder", (), {"data": "John Doe"})
    address = type("DataAttributeHolder", (), {"data": "idk some address"})

    @staticmethod
    def validate() -> bool:
        return True


class MockGetOrderForm(Mock):
    order_id = type("DataAttributeHolder", (), {"data": 1})

    @staticmethod
    def validate() -> bool:
        return True


with description("create order endpoint") as self:
    with before.all:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///spec_db"
        self.client = app.test_client()
        self.database = DatabaseAdapter(app.config["SQLALCHEMY_DATABASE_URI"])

    with after.all:
        self.database.clear_table()

    with it("tries to create an order and should fail"):
        response = self.client.post("/create", data={})
        expect(response.status_code).to(equal(400))

    with it("tries to create an order and should succeed"):
        with patch("app.CreateOrderForm", MockCreateOrderForm, create=True):
            response = self.client.post("/create")
        expect(response.status_code).to(equal(200))

    with it("tries to get an order created at previous step"):
        with patch("app.GetOrderForm", MockGetOrderForm, create=True):
            response = self.client.get("/get")
            order_xml = response.get_data(as_text=True)
            root = ET.fromstring(order_xml)
        expect(root.find("name").text).to(equal(MockCreateOrderForm.name.data))  # type: ignore
        expect(root.find("address").text).to(equal(MockCreateOrderForm.address.data))  # type: ignore
