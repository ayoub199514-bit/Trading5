"""
core/risk_manager.py
يحسب حجم الصفقة (position size) ويطبق وقف الخسارة/جني الأرباح.
"""


class RiskManager:
    def __init__(self, risk_per_trade: float, stop_loss_pct: float, take_profit_pct: float, max_open_positions: int):
        self.risk_per_trade = risk_per_trade
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        self.max_open_positions = max_open_positions

    def calc_position_size(self, balance: float, entry_price: float) -> float:
        """يحسب شحال نشريو (بالعملة الأساسية) بناء على نسبة المخاطرة."""
        risk_amount = balance * self.risk_per_trade
        stop_distance = entry_price * self.stop_loss_pct
        if stop_distance == 0:
            return 0
        position_size_quote = risk_amount / self.stop_loss_pct  # بالدولار
        position_size_base = position_size_quote / entry_price
        return round(position_size_base, 6)

    def get_stop_loss(self, entry_price: float, side: str) -> float:
        if side == "BUY":
            return entry_price * (1 - self.stop_loss_pct)
        return entry_price * (1 + self.stop_loss_pct)

    def get_take_profit(self, entry_price: float, side: str) -> float:
        if side == "BUY":
            return entry_price * (1 + self.take_profit_pct)
        return entry_price * (1 - self.take_profit_pct)

    def can_open_new_position(self, current_open_positions: int) -> bool:
        return current_open_positions < self.max_open_positions
