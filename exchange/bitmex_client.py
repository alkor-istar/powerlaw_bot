from exchange.base import ExchangeClient
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
        self.client = bitmex.bitmex(test=self.testnet, api_key=self.api_key, api_secret=self.api_secret)
        print("Connected to Bitmex exchange")

    def get_candles(self, symbol, binSize, count):
        data = self.client.Trade.Trade_getBucketed(
            symbol=symbol,
            binSize=binSize,
            count=count,
            reverse=True
        ).result()[0]
        print(data[0]['timestamp'] )

        df = pd.DataFrame([{
            'timestamp': candle['timestamp'],
            'open': candle['open'],
            'high': candle['high'],
            'low': candle['low'],
            'close': candle['close'],
            'volume': candle['volume']
        } for candle in data])

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        df.sort_index(inplace=True)
        return df

    def long(self, symbol: str, qty: float) -> None:
        self.client.Order.Order_new(symbol=symbol,side="Buy",ordType="Market",orderQty=qty).result()

    def short(self, symbol: str, qty: float) -> None:
        self.client.Order.Order_new(symbol=symbol,side="Sell",ordType="Market",orderQty=qty).result()

    def close_position(self, symbol: str) -> None:
        ammount = self.get_position_size(symbol)
        self.client.Order.Order_new(symbol=symbol,execInst="Close",ordType="Market",orderQty=-ammount).result()

    def set_stop_loss(self, symbol: str, price: float, orderQty: float) -> None:
        self.client.Order.Order_new(
            symbol=symbol,
            ordType="Stop",
            execInst="Close,MarkPrice",
            stopPx=price,
            orderQty=-orderQty
            ).result()

    def get_position_size(self, symbol: str) -> float:
        return self.client.Position.Position_get(
            filter=json.dumps({"symbol":symbol})
            ).result()[0][0]['currentQty']
        

    def get_last_price(self, symbol: str) -> float:
        return self.client.Trade.Trade_get(symbol=symbol,count=1,reverse=True).result()[0][0]['price']

    def get_total_funds(self, symbol) -> float:
        current_price = self.get_last_price(symbol) 
        margin = self.client.User.User_getMargin().result()[0]['availableMargin']
        return current_price * margin * 0.00000001
        
