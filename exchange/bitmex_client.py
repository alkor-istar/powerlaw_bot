from exchange.base import ExchangeClient
from utils.round import round_to_tick, round_down, round_up
from typing import Optional
import bitmex
import pandas as pd
import json


class BitmexClient(ExchangeClient):
    def __init__(self, api_key: str, api_secret: str, testnet: bool):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self._connect()

    def _connect(self):
        self.client = bitmex.bitmex(
            test=self.testnet, api_key=self.api_key, api_secret=self.api_secret
        )
        print("Connected to Bitmex exchange")

    def get_candles(self, symbol, binSize, count):
        data = self.client.Trade.Trade_getBucketed(
            symbol=symbol, binSize=binSize, count=count, reverse=True, partial=False
        ).result()[0]

        tick_size = self.get_tick_size(symbol)

        df = pd.DataFrame(
            [
                {
                    "timestamp": candle["timestamp"],
                    "open": round_to_tick(candle["open"], tick_size),
                    "high": round_to_tick(candle["high"], tick_size),
                    "low": round_to_tick(candle["low"], tick_size),
                    "close": round_to_tick(candle["close"], tick_size),
                    "volume": round_to_tick(candle["volume"], tick_size),
                }
                for candle in data
            ]
        )

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)
        df.sort_index(inplace=True)

        return df

    def long(self, symbol: str, qty: float) -> None:
        self.client.Order.Order_new(
            symbol=symbol, side="Buy", ordType="Market", orderQty=qty
        ).result()

    def short(self, symbol: str, qty: float) -> None:
        self.client.Order.Order_new(
            symbol=symbol, side="Sell", ordType="Market", orderQty=qty
        ).result()

    def close_position(self, symbol: str) -> None:
        ammount = self.get_position_size(symbol)
        self.client.Order.Order_new(
            symbol=symbol, execInst="Close", ordType="Market", orderQty=-ammount
        ).result()

    def set_stop_loss(
        self, symbol: str, side: str, price: float, orderQty: float
    ) -> None:
        tick_size = self.get_tick_size(symbol)
        print(
            "trying to set stop loss", side, round_up(price, tick_size), price, orderQty
        )
        self.client.Order.Order_new(
            symbol=symbol,
            ordType="Stop",
            execInst="Close,MarkPrice",
            side=side,
            stopPx=(
                91982
                # side == round_up(price, tick_size)
                # if side == "Sell"
                # else round_down(price, tick_size)
            ),
            orderQty=orderQty,
        ).result()

    def get_position_size(self, symbol: str) -> float:
        return self.client.Position.Position_get(
            filter=json.dumps({"symbol": symbol})
        ).result()[0][0]["currentQty"]

    def get_last_price(self, symbol: str) -> float:
        return self.client.Trade.Trade_get(
            symbol=symbol, count=1, reverse=True
        ).result()[0][0]["price"]

    def get_total_funds(self, symbol) -> float:
        current_price = self.get_last_price(symbol)
        margin = self.client.User.User_getMargin().result()[0]["availableMargin"]
        return current_price * margin * 0.00000001

    def get_tick_size(self, symbol):
        instrument = self.client.Instrument.Instrument_get(symbol=symbol).result()[0][0]

        return instrument["tickSize"]
