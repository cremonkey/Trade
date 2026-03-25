import datetime
from typing import Optional

class RiskManager:
    """
    Antigravity v5.0 Institutional Risk Manager.
    Enforces the Institutional Unit Model and Discipline Locks.
    """
    
    def __init__(
        self, 
        starting_balance: float = 88.0, 
        unit_scale: float = 0.01, 
        unit_step: float = 100.0,
        lot_cap: float = 5.0
    ):
        self.starting_balance = starting_balance
        self.unit_scale = unit_scale
        self.unit_step = unit_step
        self.lot_cap = lot_cap

    def calculate_lot_size(self, equity: float) -> float:
        """
        Calculates allowable sizing based on the Institutional Unit Model.
        - 0.01 lot per $100 equity (until $1,000)
        - 0.10 lot per $1,000 equity (above $1,000)
        """
        if equity < 1000:
            lots = (equity / self.unit_step) * self.unit_scale
        else:
            lots = (equity / 1000.0) * 0.10
            
        # Enforce Absolute Cap
        return min(round(lots, 2), self.lot_cap)

    def validate_volatility(self, m5_atr: float) -> bool:
        """
        Volatility Filter: Halt execution if M5 ATR is above 10.0 gold points.
        """
        return m5_atr < 10.0

    def is_discipline_locked(self, lock_until: Optional[datetime.datetime]) -> bool:
        """
        Checks if a Discipline Lock is active.
        """
        if not lock_until:
            return False
        return datetime.datetime.now(datetime.timezone.utc) < lock_until

    def get_opex_deduction(self, daily_pnl: float) -> float:
        """
        Daily Operational Margin ($5 - $30) before net compounding is recorded.
        """
        if daily_pnl <= 0:
            return 0.0
        # Simple logic: 10% of profit, capped between $5 and $30
        return max(5.0, min(30.0, daily_pnl * 0.1))
