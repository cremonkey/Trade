from __future__ import annotations

import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv


load_dotenv()

TD_BASE = "https://api.twelvedata.com"
TD_KEY = os.environ.get("TWELVEDATA_API_KEY")


def td_get(endpoint: str, params: dict | None = None) -> dict:
    params = params or {}
    params["apikey"] = TD_KEY
    response = requests.get(f"{TD_BASE}/{endpoint}", params=params, timeout=20)
    data = response.json()
    if data.get("code") == 429:
        raise Exception("RATE_LIMIT: Credits exhausted. Wait 60s.")
    if data.get("status") == "error":
        raise Exception(f"TD_ERROR: {data.get('message')}")
    return data


def td_get_soft(endpoint: str, params: dict | None = None) -> dict:
    params = params or {}
    params["apikey"] = TD_KEY
    response = requests.get(f"{TD_BASE}/{endpoint}", params=params, timeout=20)
    return response.json()


def get_primary_prices() -> dict:
    prices = {"XAU/USD": td_get("price", {"symbol": "XAU/USD", "dp": 4})}
    xag_data = td_get_soft("price", {"symbol": "XAG/USD", "dp": 4})
    if xag_data.get("status") == "error":
        prices["XAG/USD"] = {
            "status": "unavailable",
            "message": xag_data.get("message", "XAG/USD unavailable on current plan."),
        }
    else:
        prices["XAG/USD"] = xag_data
    return prices


def full_analysis_cycle() -> dict:
    return {
        "m15": td_get(
            "time_series",
            {"symbol": "XAU/USD", "interval": "15min", "outputsize": 100, "dp": 2, "timezone": "UTC"},
        ),
        "daily": td_get(
            "time_series",
            {"symbol": "XAU/USD", "interval": "1day", "outputsize": 60, "dp": 2, "timezone": "UTC"},
        ),
        "h4": td_get(
            "time_series",
            {"symbol": "XAU/USD", "interval": "4h", "outputsize": 50, "dp": 2, "timezone": "UTC"},
        ),
        "h1": td_get(
            "time_series",
            {"symbol": "XAU/USD", "interval": "1h", "outputsize": 100, "dp": 2, "timezone": "UTC"},
        ),
        "atr": td_get(
            "atr",
            {"symbol": "XAU/USD", "interval": "5min", "time_period": 14, "dp": 2, "timezone": "UTC"},
        ),
        "rsi": td_get(
            "rsi",
            {"symbol": "XAU/USD", "interval": "1h", "time_period": 14, "dp": 2, "timezone": "UTC"},
        ),
        "prices": get_primary_prices(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
