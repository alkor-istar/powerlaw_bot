from abc import ABC, abstractmethod
from typing import Optional


class ExchangeClient(ABC):
    @abstractmethod
    def get_candles(self, symbol: str, binSize: str, count: int):
        pass

    @abstractmethod
    def long(self, symbol: str, qty: float) -> None:
        pass

    @abstractmethod
    def short(self, symbol: str, qty: float) -> None:
        pass

    @abstractmethod
    def close_position(self, symbol: str) -> None:
        pass

    @abstractmethod
    def set_stop_loss(
        self,
        symbol: str,
        side: str,
        price: float,
        orderQty: float,
        reduce_only: bool = True,
    ) -> None:
        pass

    @abstractmethod
    def get_position_size(self, symbol: str) -> float:
        pass

    @abstractmethod
    def get_last_price(self, symbol: str) -> float:
        pass

    @abstractmethod
    def get_total_funds(self, symbol: str) -> float:
        pass

    @abstractmethod
    def get_tick_size(self, symbol: str) -> float:
        pass

    @abstractmethod
    def amend_stop_loss(self, orderID: str, price: float, orderQty: float) -> None:
        pass

    @abstractmethod
    def close_all_positions(self, symbol: str) -> None:
        pass
