"""
core/paper_broker.py
"وسيط وهمي" — يحاكي التداول الحقيقي (يشري ويبيع) بلا فلوس حقيقية.
يفيد باش تجرب البوت وتشوف كيفاش رح يربح/يخسر قبل ما تخاطر بفلوس حقيقية.
"""

import json
from datetime import datetime, timezone


class PaperBroker:
    def __init__(self, starting_balance: float, log_file: str = "logs/paper_trades.json"):
        self.balance = starting_balance
        self.starting_balance = starting_balance
        self.open_positions = {}   # symbol -> position dict
        self.trade_history = []
        self.log_file = log_file

    def open_position(self, symbol: str, side: str, size: float, entry_price: float,
                       stop_loss: float, take_profit: float):
        self.open_positions[symbol] = {
            "side": side,
            "size": size,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "opened_at": datetime.now(timezone.utc).isoformat(),
        }
        self._log_event("OPEN", symbol, side, size, entry_price)

    def check_and_close_positions(self, symbol: str, current_price: float):
        """يتفقد واش وصلنا لـ stop-loss ولا take-profit ويسكر الصفقة تلقائيا."""
        pos = self.open_positions.get(symbol)
        if not pos:
            return None

        side = pos["side"]
        hit_sl = (side == "BUY" and current_price <= pos["stop_loss"]) or \
                 (side == "SELL" and current_price >= pos["stop_loss"])
        hit_tp = (side == "BUY" and current_price >= pos["take_profit"]) or \
                 (side == "SELL" and current_price <= pos["take_profit"])

        if hit_sl or hit_tp:
            return self._close_position(symbol, current_price, "STOP_LOSS" if hit_sl else "TAKE_PROFIT")
        return None

    def _close_position(self, symbol: str, exit_price: float, reason: str):
        pos = self.open_positions.pop(symbol)
        entry = pos["entry_price"]
        size = pos["size"]

        if pos["side"] == "BUY":
            pnl = (exit_price - entry) * size
        else:
            pnl = (entry - exit_price) * size

        self.balance += pnl
        record = {
            "symbol": symbol, "side": pos["side"], "entry": entry,
            "exit": exit_price, "size": size, "pnl": round(pnl, 2),
            "reason": reason, "balance_after": round(self.balance, 2),
            "closed_at": datetime.now(timezone.utc).isoformat(),
        }
        self.trade_history.append(record)
        self._log_event("CLOSE", symbol, pos["side"], size, exit_price, pnl=pnl, reason=reason)
        return record

    def get_open_positions_count(self) -> int:
        return len(self.open_positions)

    def get_summary(self) -> dict:
        total_pnl = self.balance - self.starting_balance
        wins = [t for t in self.trade_history if t["pnl"] > 0]
        return {
            "balance": round(self.balance, 2),
            "total_pnl": round(total_pnl, 2),
            "total_pnl_pct": round((total_pnl / self.starting_balance) * 100, 2),
            "total_trades": len(self.trade_history),
            "win_rate": round(len(wins) / len(self.trade_history) * 100, 1) if self.trade_history else 0,
        }

    def _log_event(self, event_type, symbol, side, size, price, pnl=None, reason=None):
        entry = {
            "event": event_type, "symbol": symbol, "side": side,
            "size": size, "price": price, "pnl": pnl, "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except FileNotFoundError:
            pass  # logs/ folder غير موجود، تجاهل بصمت
