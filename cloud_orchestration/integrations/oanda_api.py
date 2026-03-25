import os
import httpx
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
        Get real-time spot price via httpx.
        """
        params = {
            "base": base,
            "quote": quotes,
            "data_set": "OANDA",
            "decimal_places": "5"
        }

        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{self.BASE_URL}/v2/rates/spot.json",
                headers=self.headers,
                params=params
            )
            r.raise_for_status()
            return r.json()

    async def get_market_data(self) -> Dict[str, Optional[float]]:
        """
        Returns spot prices for XAU/USD, XAG/USD, and calculated DXY.
        """
        prices = {"XAU/USD": 0.0, "XAG/USD": 0.0, "DXY": 0.0}
        
        if not self.api_key:
            return prices

        try:
            # 1. Gold (XAU/USD)
            gold = await self.get_spot("XAU", ["USD"])
            prices["XAU/USD"] = float(gold["quotes"][0]["midpoint"])
            
            # 2. Silver (XAG/USD)
            silver = await self.get_spot("XAG", ["USD"])
            prices["XAG/USD"] = float(silver["quotes"][0]["midpoint"])
            
            # 3. DXY Calculation
            prices["DXY"] = await self._calculate_dxy()
            
        except Exception as e:
            print(f"[OandaAPI] Error: {e}")
            
        return prices

    async def _calculate_dxy(self) -> float:
        """
        DXY = 50.14348112 x EURUSD^(-0.576) x USDJPY^(0.136) x GBPUSD^(-0.119)
              x USDCAD^(0.091) x USDSEK^(0.042) x USDCHF^(0.036)
        """
        try:
            # Fetch all basket pairs
            usd_basket = await self.get_spot("USD", ["JPY", "CAD", "SEK", "CHF"])
            eur = await self.get_spot("EUR", ["USD"])
            gbp = await self.get_spot("GBP", ["USD"])
            
            # Map values
            eurusd = float(eur["quotes"][0]["midpoint"])
            gbpusd = float(gbp["quotes"][0]["midpoint"])
            
            usd_rates = {q['quote_currency']: float(q['midpoint']) for q in usd_basket['quotes']}
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
            print(f"[OandaAPI] DXY Calc Error: {e}")
            return 0.0
