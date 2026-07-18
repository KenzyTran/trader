import hashlib
import math
from datetime import datetime, timezone

from massive import RESTClient

from .config import settings


def simulated_price(symbol: str) -> float:
    """Stable intraday simulation, unique per symbol."""
    seed = int(hashlib.sha256(symbol.upper().encode()).hexdigest()[:8], 16)
    minute = int(datetime.now(timezone.utc).timestamp() // 60)
    return round(20 + seed % 280 + math.sin(minute / 17 + seed) * 4, 2)


def get_share_price(symbol: str) -> float:
    symbol = symbol.strip().upper()
    if not symbol:
        raise ValueError("Symbol cannot be empty")
    if settings.massive_api_key:
        try:
            return float(RESTClient(settings.massive_api_key).get_previous_close_agg(symbol)[0].close)
        except Exception as exc:
            print(f"Market API unavailable ({exc}); using simulation")
    return simulated_price(symbol)


def is_market_open() -> bool:
    if not settings.massive_api_key:
        return True
    try:
        return RESTClient(settings.massive_api_key).get_market_status().market == "open"
    except Exception:
        return True
