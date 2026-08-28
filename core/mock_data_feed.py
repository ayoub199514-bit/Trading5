"""
core/mock_data_feed.py

يولد بيانات أسعار وهمية (Random Walk واقعي) باش تقدر تجرب البوت
كاملا (Paper Trading) بلا حتى حساب/API عند أي منصة.

باش تربطو ببيانات حقيقية، بدل PAPER_TRADING = False فـ config.py
وحط API Key/Secret ديالك — البوت غادي يستعمل core/data_feed.py (ccxt) تلقائيا.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone


class MockDataFeed:
    def __init__(self, seed: int = None):
        self._prices = {}  # symbol -> last simulated price
        self._rng = np.random.default_rng(seed)

    def fetch_ohlcv(self, symbol: str, timeframe: str = "1h", limit: int = 500) -> pd.DataFrame:
        if symbol not in self._prices:
            self._prices[symbol] = 30000.0 if "BTC" in symbol else 2000.0

        base_price = self._prices[symbol]
        # Random walk بسيط مع "trend" و"noise" باش يبان واقعي شوية
        returns = self._rng.normal(loc=0.0002, scale=0.01, size=limit)
        prices = base_price * np.cumprod(1 + returns)

        now = datetime.now(timezone.utc)
        timestamps = [now - timedelta(hours=(limit - i)) for i in range(limit)]

        df = pd.DataFrame({
            "timestamp": timestamps,
            "open": prices * (1 - self._rng.uniform(0, 0.002, limit)),
            "high": prices * (1 + self._rng.uniform(0, 0.004, limit)),
            "low": prices * (1 - self._rng.uniform(0, 0.004, limit)),
            "close": prices,
            "volume": self._rng.uniform(10, 500, limit),
        })

        self._prices[symbol] = float(prices[-1])
        return df

    def fetch_ticker_price(self, symbol: str) -> float:
        return self._prices.get(symbol, 30000.0)
