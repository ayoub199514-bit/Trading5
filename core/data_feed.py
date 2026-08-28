"""
core/data_feed.py
يتصل بمنصة التداول (عبر ccxt) ويجيب بيانات الشموع (OHLCV) التاريخية والحية.
"""

import pandas as pd

try:
    import ccxt
except ImportError:
    ccxt = None


class DataFeed:
    def __init__(self, exchange_name: str, api_key: str = "", api_secret: str = "", testnet: bool = True):
        if ccxt is None:
            raise ImportError(
                "مكتبة ccxt ماهياش مثبتة. ثبتها بـ: pip install ccxt"
            )

        exchange_class = getattr(ccxt, exchange_name)
        self.exchange = exchange_class({
            "apiKey": api_key,
            "secret": api_secret,
            "enableRateLimit": True,
        })

        if testnet and hasattr(self.exchange, "set_sandbox_mode"):
            self.exchange.set_sandbox_mode(True)

    def fetch_ohlcv(self, symbol: str, timeframe: str = "1h", limit: int = 500) -> pd.DataFrame:
        """يرجع DataFrame فيه: timestamp, open, high, low, close, volume"""
        raw = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(raw, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df

    def fetch_ticker_price(self, symbol: str) -> float:
        ticker = self.exchange.fetch_ticker(symbol)
        return float(ticker["last"])
