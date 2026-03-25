from __future__ import annotations

import math

import twelve_data_client


def calculate_dxy(prices: dict[str, float]) -> float | None:
    """
    Synthetic DXY approximation:
    DXY = 50.14348112 * (EURUSD^-0.576) * (USDJPY^0.136) * (GBPUSD^-0.119)
          * (USDCAD^0.091) * (USDSEK^0.042) * (USDCHF^0.036)
    """
    try:
        eurusd = prices.get("EUR/USD")
        usdjpy = prices.get("USD/JPY")
        gbpusd = prices.get("GBP/USD")
        usdcad = prices.get("USD/CAD")
        usdsek = prices.get("USD/SEK")
        usdchf = prices.get("USD/CHF")

        dxy = (
            50.14348112
            * math.pow(eurusd, -0.576)
            * math.pow(usdjpy, 0.136)
            * math.pow(gbpusd, -0.119)
            * math.pow(usdcad, 0.091)
            * math.pow(usdsek, 0.042)
            * math.pow(usdchf, 0.036)
        )
        return round(dxy, 3)
    except Exception as exc:
        print(f"DXY calculation error: {exc}")
        return None


def get_live_dxy() -> float | None:
    symbols = "EUR/USD,USD/JPY,GBP/USD,USD/CAD,USD/SEK,USD/CHF"
    data = twelve_data_client.td_get("price", {"symbol": symbols})
    prices = {symbol: float(payload["price"]) for symbol, payload in data.items()}
    return calculate_dxy(prices)


if __name__ == "__main__":
    dxy_val = get_live_dxy()
    if dxy_val is not None:
        print("--- DXY CALCULATOR (v4.4) ---")
        print(f"Current Synthetic DXY: {dxy_val}")
