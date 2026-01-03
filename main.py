import time
from exchange.factory import create_exchange
from strategy.powerlaw import PowerlawStrategy
from indicators.bollinger import bollinger_bands
from utils.time import seconds_until_next_candle

SYMBOL = "XBTUSD"
TIMEFRAME = "1h"
TIMEFRAME_SECONDS = 300
CANDLE_COUNT = 50

def main():
    exchange = create_exchange("bitmex")
    strategy = PowerlawStrategy()

    print("🚀 Bot started")

    while True:
        # wait = seconds_until_next_candle(TIMEFRAME_SECONDS)
        # print(f"⏳ Waiting {wait}s for candle close")
        # time.sleep(wait + 1)

        df = exchange.get_candles(SYMBOL, TIMEFRAME, CANDLE_COUNT)
        # print(df.iloc[:-1])  # drop unfinished candle

        df = bollinger_bands(df)

        position = exchange.get_position_size(SYMBOL)
        signal = strategy.evaluate(df, position)

        if signal == "long":
            print("📈 Enter LONG")
        #     exchange.open_long(SYMBOL)

        elif signal == "short":
            print("📉 Enter SHORT")
        #     exchange.open_short(SYMBOL)

        elif signal == "exit":
            print("❌ Exit position")
        #     exchange.close_position(SYMBOL)


if __name__ == "__main__":
    main() 