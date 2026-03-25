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
        self.tv_feed = None # Dynamic import to avoid pandas overhead if not used

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

    async def _fetch_from_tv(self) -> Dict[str, Optional[float]]:
        """
        Fallback to TradingView unofficial datafeed.
        """
        try:
            from tvDatafeed import TvDatafeed, Interval
            tv = TvDatafeed()
            gold = tv.get_hist(symbol="XAUUSD", exchange="OANDA", interval=Interval.in_1_minute, n_bars=1)
            silver = tv.get_hist(symbol="XAGUSD", exchange="OANDA", interval=Interval.in_1_minute, n_bars=1)
            dxy = tv.get_hist(symbol="DXY", exchange="TVC", interval=Interval.in_1_minute, n_bars=1)
            
            return {
                "XAU/USD": gold['close'].iloc[-1] if not gold.empty else 0.0,
                "XAG/USD": silver['close'].iloc[-1] if not silver.empty else 0.0,
                "DXY": dxy['close'].iloc[-1] if not dxy.empty else 0.0
            }
        except Exception as e:
            print(f"[{datetime.now()}] MarketDataHub: TVDatafeed Critical Failure: {e}")
            return {"XAU/USD": 0.0, "XAG/USD": 0.0, "DXY": 0.0}
