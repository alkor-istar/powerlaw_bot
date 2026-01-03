from exchange.base import ExchangeClient
from exchange.bitmex_client import BitmexClient
from config.bitmex import API_KEY, API_SECRET, TESTNET


def create_exchange(name: str) -> ExchangeClient:
    if name.lower() == "bitmex":
        return BitmexClient(
            api_key=API_KEY,
            api_secret=API_SECRET,
            testnet=TESTNET
        )

    raise ValueError(f"Unsupported exchange: {name}")
