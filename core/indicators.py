"""
core/indicators.py
مؤشرات تقنية (Technical Indicators) تستعمل كـ "features" للاستراتيجية يلي تتعلم.
"""

import pandas as pd
import numpy as np


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # المتوسطات المتحركة
    df["sma_10"] = df["close"].rolling(10).mean()
    df["sma_30"] = df["close"].rolling(30).mean()
    df["ema_12"] = df["close"].ewm(span=12, adjust=False).mean()
    df["ema_26"] = df["close"].ewm(span=26, adjust=False).mean()

    # MACD
    df["macd"] = df["ema_12"] - df["ema_26"]
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()

    # RSI
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    df["rsi_14"] = 100 - (100 / (1 + rs))

    # التقلب (Volatility) وBollinger Bands
    df["volatility_20"] = df["close"].rolling(20).std()
    df["bb_mid"] = df["close"].rolling(20).mean()
    df["bb_upper"] = df["bb_mid"] + 2 * df["volatility_20"]
    df["bb_lower"] = df["bb_mid"] - 2 * df["volatility_20"]

    # التغير النسبي (يفيد كـ label للتعلم)
    df["return_next"] = df["close"].shift(-1) / df["close"] - 1

    return df.dropna().reset_index(drop=True)
