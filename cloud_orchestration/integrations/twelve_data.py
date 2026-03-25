import os
import httpx
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class TwelveDataIntegration:
    """
    Wrapper for Twelve Data API to fetch live XAU/USD, DXY, and XAG/USD.
    """
    
    def __init__(self):
        self.api_key = os.getenv("TWELVE_DATA_API_KEY", "")
        self.base_url = "https://api.twelvedata.com"

    async def get_price(self, symbol: str) -> Optional[float]:
        """
        Fetches the real-time price for a symbol.
        """
        if not self.api_key:
            return None
            
        params = {
            "symbol": symbol,
            "apikey": self.api_key
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/price", params=params)
            if response.status_code == 200:
                data = response.json()
                price = data.get("price")
                if price is not None:
                    return float(price)
                else:
                    print(f"[TwelveData] Error for {symbol}: {data}")
                    return 0.0
        return None

    async def get_market_data(self) -> Dict[str, Optional[float]]:
        """
        Consolidated fetch for XAU/USD, XAG/USD, and DXY/Proxies.
        """
        # Try DXY, fallback to USD/JPY as a proxy if DXY is restricted.
        symbols = ["XAU/USD", "XAG/USD", "DXY", "USD/JPY"] 
        results = {}
        for symbol in symbols:
            try:
                price = await self.get_price(symbol)
                results[symbol] = price if price else 0.0
            except Exception:
                results[symbol] = 0.0
        
        # Heuristic Logic for SMT: Ensure we have Silver and a Dollar proxy
        if not results.get("XAG/USD") or results["XAG/USD"] == 0.0:
            print("[TwelveData] SMT Alert: Silver price missing or restricted.")
            
        return results
