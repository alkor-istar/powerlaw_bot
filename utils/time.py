import time
from datetime import datetime, timezone

def seconds_until_next_candle(timeframe_seconds: int) -> int:
    now = datetime.now(timezone.utc).timestamp()
    return int(timeframe_seconds - (now % timeframe_seconds))
