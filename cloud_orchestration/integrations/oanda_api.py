import os
import httpx
import asyncio
from datetime import datetime
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class OandaSpotPrices:
    """
    Antigravity v5.5 OANDA High-Fidelity Integration.
    Fetches real-time SPOT prices from OANDA Exchange Rates API.
    Includes automated DXY calculation from the 6-currency basket.
    """

    BASE_URL = "https://exchange-rates-api.oanda.com"

    def __init__(self):
        self.api_key = os.getenv("OANDA_API_KEY", "")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def get_spot(self, base: str, quotes: list) -> Dict:
        """
        Get real-time spot price via httpx with timeout.
        """
        params = {
            "base": base,
            "quote": quotes,
            "data_set": "OANDA",
            "decimal_places": "5"
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(
                f"{self.BASE_URL}/v2/rates/spot.json",
                headers=self.headers,
                params=params
            )
            r.raise_for_status()
            return r.json()

    async def get_market_data(self) -> Dict[str, Optional[float]]:
        """
        Returns spot prices for XAU/USD, XAG/USD, and calculated DXY using parallel fetching.
        """
        prices = {"XAU/USD": 0.0, "XAG/USD": 0.0, "DXY": 0.0}
        
        if not self.api_key:
            return prices

        try:
            print(f"[{datetime.now()}] OandaAPI: Parallel Scan Initiated...")
            
            # Fetch Gold, Silver, and DXY Trigger in parallel
            task_gold = self.get_spot("XAU", ["USD"])
            task_silver = self.get_spot("XAG", ["USD"])
            task_dxy = self._calculate_dxy()
            
            gold_res, silver_res, dxy_val = await asyncio.gather(task_gold, task_silver, task_dxy)
            
            prices["XAU/USD"] = float(gold_res["quotes"][0]["midpoint"])
            prices["XAG/USD"] = float(silver_res["quotes"][0]["midpoint"])
            prices["DXY"] = dxy_val
            
            print(f"[{datetime.now()}] OandaAPI: Scan Complete (XAU: {prices['XAU/USD']})")
            
        except Exception as e:
            print(f"[{datetime.now()}] OandaAPI: Failure: {e}")
            
        return prices

    async def _calculate_dxy(self) -> float:
        """
        Parallel DXY Calculation from Currency Basket.
        """
        try:
            # Parallel fetch for the basket
            task_basket = self.get_spot("USD", ["JPY", "CAD", "SEK", "CHF"])
            task_eur = self.get_spot("EUR", ["USD"])
            task_gbp = self.get_spot("GBP", ["USD"])
            
            basket_res, eur_res, gbp_res = await asyncio.gather(task_basket, task_eur, task_gbp)
            
            # Map values
            eurusd = float(eur_res["quotes"][0]["midpoint"])
            gbpusd = float(gbp_res["quotes"][0]["midpoint"])
            
            usd_rates = {q['quote_currency']: float(q['midpoint']) for q in basket_res['quotes']}
            usdjpy = usd_rates["JPY"]
            usdcad = usd_rates["CAD"]
            usdsek = usd_rates["SEK"]
            usdchf = usd_rates["CHF"]
            
            # Formula execution
            dxy = (50.14348112
                   * (eurusd ** -0.576)
                   * (usdjpy ** 0.136)
                   * (gbpusd ** -0.119)
                   * (usdcad ** 0.091)
                   * (usdsek ** 0.042)
                   * (usdchf ** 0.036))
            
            return round(dxy, 3)
        except Exception as e:
            print(f"[{datetime.now()}] OandaAPI: DXY Error: {e}")
            return 0.0
