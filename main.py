import time
from exchange.factory import create_exchange
from strategy.powerlaw import PowerlawStrategy
from utils.time import seconds_until_next_candle

SYMBOL = "XBTUSD"
TIMEFRAME = "5m"
TIMEFRAME_SECONDS = 300
CANDLE_COUNT = 50


def main():
    print("Bot started")
    exchange = create_exchange("bitmex")
    strategy = PowerlawStrategy()

    while True:
        wait = seconds_until_next_candle(TIMEFRAME_SECONDS)
        print(f"Waiting {wait}s for candle close")
        time.sleep(wait + 1)

        strategy.trade(exchange, SYMBOL, TIMEFRAME, CANDLE_COUNT)


if __name__ == "__main__":
    main()
