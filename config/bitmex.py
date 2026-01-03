import os
from dotenv import load_dotenv


load_dotenv()

TESTNET = os.getenv("BITMEX_TESTNET", "false").lower() == "true"
API_KEY = os.getenv("BITMEX_API_KEY")
API_SECRET = os.getenv("BITMEX_API_SECRET")

if not API_KEY or not API_SECRET:
    raise RuntimeError("Missing BitMEX API credentials")

        