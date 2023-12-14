from abc import ABC, abstractmethod

from src.domain.order import Order


class DatabasePort(ABC):
    @abstractmethod
    def create_order(self, order: Order) -> None:
        pass
