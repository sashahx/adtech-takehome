from dataclasses import asdict
from typing import Any, Dict, Optional

from sqlalchemy import (
    Column,
    DateTime,
    Engine,
    Integer,
    MetaData,
    Table,
    Text,
    create_engine,
    delete,
    func,
)

from src.domain.order import Order
from src.ports.database_ports import DatabasePort


def create_table(table: Table, engine: Engine) -> None:
    table.create(engine, checkfirst=True)


orders = Table(
    "orders",
    MetaData(),
    Column("id", Integer, primary_key=True),
    Column("name", Text(200), nullable=False),
    Column("address", Text(200), nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
    Column(
        "updated_at",
        DateTime,
        nullable=False,
        server_default=func.now(),
    ),
)


class DatabaseAdapter(DatabasePort):
    def __init__(self, database_uri: str) -> None:
        engine = create_engine(database_uri)
        create_table(orders, engine)
        self.connection = engine.connect()

    def create_order(self, order: Order) -> None:
        with self.connection.begin():
            self.connection.execute(orders.insert(), asdict(order))

    def get_order(self, order_id: int) -> Optional[Dict[str, Any]]:
        with self.connection.begin():
            result = self.connection.execute(
                orders.select().where(orders.c.id == order_id)
            ).first()
            if result:
                return dict(result._mapping)
            return None

    def clear_table(self) -> None:
        with self.connection.begin():
            self.connection.execute(delete(orders))
