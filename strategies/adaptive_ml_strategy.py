"""
strategies/adaptive_ml_strategy.py

استراتيجية "تتعلم": تستعمل نموذج تعلم آلي (Random Forest) باش تتوقع
واش السعر غادي يطلع ولا ينزل، وتتحسن (retrain) كل ما جبنا بيانات جديدة.

هادي نقطة انطلاق بسيطة — تقدر تبدلها بنماذج أعقد (XGBoost, LSTM...) فيما بعد.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

FEATURE_COLUMNS = [
    "sma_10", "sma_30", "ema_12", "ema_26",
    "macd", "macd_signal", "rsi_14",
    "volatility_20", "bb_upper", "bb_lower",
]


class AdaptiveMLStrategy:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=6,
            random_state=42,
        )
        self.is_trained = False
        self.last_accuracy = None

    def _build_labels(self, df: pd.DataFrame) -> pd.Series:
        # 1 = السعر غادي يطلع فالشمعة الجاية، 0 = غادي ينزل ولا يبقى
        return (df["return_next"] > 0).astype(int)

    def train(self, df: pd.DataFrame):
        """تدرب (أو تعيد تدريب) النموذج على البيانات التاريخية."""
        X = df[FEATURE_COLUMNS]
        y = self._build_labels(df)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, shuffle=False  # shuffle=False مهم فبيانات زمنية
        )

        self.model.fit(X_train, y_train)
        preds = self.model.predict(X_test)
        self.last_accuracy = accuracy_score(y_test, preds)
        self.is_trained = True

        return self.last_accuracy

    def predict_signal(self, latest_row: pd.Series) -> dict:
        """
        يرجع إشارة تداول بناء على آخر شمعة:
        {"action": "BUY" | "SELL" | "HOLD", "confidence": float}
        """
        if not self.is_trained:
            return {"action": "HOLD", "confidence": 0.0}

        X = latest_row[FEATURE_COLUMNS].to_frame().T
        proba = self.model.predict_proba(X)[0]  # [P(نزول), P(طلوع)]
        prob_up = proba[1]

        # عتبة قرار — تقدر تعدلها حسب مدى تحفظك
        if prob_up > 0.60:
            return {"action": "BUY", "confidence": round(prob_up, 3)}
        elif prob_up < 0.40:
            return {"action": "SELL", "confidence": round(1 - prob_up, 3)}
        else:
            return {"action": "HOLD", "confidence": round(prob_up, 3)}
