from datetime import datetime
from typing import Dict, Optional
from integrations.yahoo_finance import YahooFinanceIntegration
from integrations.twelve_data import TwelveDataIntegration
from integrations.oanda_api import OandaSpotPrices

class MarketDataHub:
    """
    Antigravity v5.5 Redundant Market Data Orchestrator.
    Strategy: OANDA (Institutional) -> Yahoo Finance (Primary) -> Twelve Data (Backup).
    """
    
    def __init__(self):
        self.oanda = OandaSpotPrices()
        self.yahoo = YahooFinanceIntegration()
        self.twelve = TwelveDataIntegration()

    async def get_market_data(self) -> Dict[str, Optional[float]]:
        """
        Fetches the Triple-Asset Matrix with multi-level fallback.
        """
        print(f"[{datetime.now()}] MarketDataHub: Scanning OANDA (Institutional Tier)...")
        results = await self.oanda.get_market_data()
        
        # Check if Institutional failed
        if results.get("XAU/USD", 0.0) == 0.0:
            print(f"[{datetime.now()}] MarketDataHub: OANDA Failed. Switching to Yahoo Finance (Primary)...")
            results = await self.yahoo.get_market_data()
        
        # Check if Primary failed
        if results.get("XAU/USD", 0.0) == 0.0:
            print(f"[{datetime.now()}] MarketDataHub: Yahoo Failed. Switching to Twelve Data (Backup)...")
            results = await self.twelve.get_market_data()
            
        return results
