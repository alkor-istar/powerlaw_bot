import time
from exchange.factory import create_exchange
from strategy.powerlaw import PowerlawStrategy
from indicators.bollinger import bollinger_bands
from utils.time import seconds_until_next_candle

SYMBOL = "XBTUSD"
TIMEFRAME = "5m"
TIMEFRAME_SECONDS = 300
CANDLE_COUNT = 50


def main():
    exchange = create_exchange("bitmex")
    strategy = PowerlawStrategy()

    print("Bot started")

    while True:
        wait = seconds_until_next_candle(TIMEFRAME_SECONDS)
        print(f"Waiting {wait}s for candle close")
        time.sleep(wait + 1)

        df = exchange.get_candles(SYMBOL, TIMEFRAME, CANDLE_COUNT)
        df = bollinger_bands(df)

        position = exchange.get_position_size(SYMBOL)
        signal, stoploss = strategy.evaluate(df, position)

        if signal == "long":
            print("Enter LONG")
            exchange.long(SYMBOL, 100)
            exchange.set_stop_loss(
                symbol=SYMBOL, side="Sell", price=stoploss, orderQty=100
            )
        elif signal == "short":
            print("Enter SHORT")
            exchange.short(SYMBOL, 100)
            print(stoploss)
            exchange.set_stop_loss(
                symbol=SYMBOL, side="Buy", price=stoploss, orderQty=100
            )
        elif signal == "movesl":
            print("Move SL")
            exchange.set_stop_loss(
                symbol=SYMBOL, side="Buy", price=stoploss, orderQty=100
            )
            exchange.set_stop_loss(
                symbol=SYMBOL, side="Sell", price=stoploss, orderQty=100
            )


if __name__ == "__main__":
    main()
