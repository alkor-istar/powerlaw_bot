import time
from utils.logger import Logger
from exchange.factory import create_exchange
from strategy.powerlaw import PowerlawStrategy
from utils.time import seconds_until_next_candle
import config.warning
import signal
import threading

SYMBOL = "XBTUSD"
TIMEFRAME = "5m"
TIMEFRAME_SECONDS = 300
CANDLE_COUNT = 50

shutdown_event = threading.Event()


def handle_signal(signum, frame):
    shutdown_event.set()


signal.signal(signal.SIGINT, handle_signal)


def main():
    logger = Logger()
    logger.log("Bot started")
    exchange = create_exchange("bitmex")
    strategy = PowerlawStrategy(logger)

    while not shutdown_event.is_set():
        wait = seconds_until_next_candle(TIMEFRAME_SECONDS)
        logger.log(f"Waiting {wait}s for candle close")

        # Wait for candle OR shutdown
        if shutdown_event.wait(wait + 1):
            break

        strategy.trade(exchange, SYMBOL, TIMEFRAME, CANDLE_COUNT)

    logger.log("Shutting down bot cleanly")
    exchange.close_all_positions(symbol=SYMBOL)


if __name__ == "__main__":
    main()
