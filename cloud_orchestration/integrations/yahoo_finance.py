import httpx
from datetime import datetime
from typing import Dict, Optional

class YahooFinanceIntegration:
    """
    Sovereign Market Data Provider using Yahoo Finance.
    Provides free real-time access to XAU, XAG, and DXY.
    """
    
    def __init__(self):
        self.symbols = {
            "XAU/USD": "GC=F",      # Gold Futures
            "XAG/USD": "SI=F",      # Silver Futures
            "DXY":     "DX-Y.NYB"   # US Dollar Index
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    async def get_market_data(self) -> Dict[str, Optional[float]]:
        """
        Fetches the Triple-Asset Matrix (Gold, Silver, DXY) with timeout.
        """
        tickers = ",".join(self.symbols.values())
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={tickers}"
        
        results = {
            "XAU/USD": 0.0,
            "XAG/USD": 0.0,
            "DXY": 0.0
        }
        
        try:
            print(f"[{datetime.now()}] YahooFinance: Initiating Triple-Asset Scan...")
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, headers=self.headers)
                if response.status_code == 200:
                    data = response.json()
                    for quote in data.get("quoteResponse", {}).get("result", []):
                        # Map Yahoo symbols back to our institutional symbols
                        for friendly_name, yahoo_symbol in self.symbols.items():
                            if quote.get("symbol") == yahoo_symbol:
                                results[friendly_name] = round(quote.get("regularMarketPrice", 0.0), 4)
                    print(f"[{datetime.now()}] YahooFinance: Scan Successful.")
                else:
                    print(f"[{datetime.now()}] YahooFinance: HTTP Error {response.status_code}")
        except Exception as e:
            print(f"[{datetime.now()}] YahooFinance: Error during scan: {e}")
            
        return results
