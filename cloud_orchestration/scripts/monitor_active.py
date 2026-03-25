from __future__ import annotations

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright


ROOT_DIR = Path(__file__).resolve().parents[1]
CHARTS_DIR = ROOT_DIR / "charts"
TMP_DIR = ROOT_DIR / "tmp"
sys.path.append(str(ROOT_DIR))

from find_cdp import find_cdp_endpoint


async def monitor_gold() -> None:
    cdp_endpoint = os.getenv("CDP_ENDPOINT") or find_cdp_endpoint() or "http://127.0.0.1:9222"
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting Lean Gold Monitor...")

    async with async_playwright() as playwright:
        try:
            browser = await playwright.chromium.connect_over_cdp(cdp_endpoint)
            if not browser or not browser.contexts:
                print("Monitor error: browser context not reachable.")
                return

            context = browser.contexts[0]
            gold_page = None
            for page in context.pages:
                title = await page.title()
                if any(token in title.upper() for token in ["XAUUSD", "GOLD", "XAU / USD"]):
                    gold_page = page
                    break

            if not gold_page:
                for page in context.pages:
                    if "tradingview.com" in page.url:
                        gold_page = page
                        break

            if not gold_page:
                print("Monitor error: no TradingView gold tab available.")
                return

            await gold_page.bring_to_front()
            await gold_page.keyboard.press("Escape")
            await gold_page.mouse.click(500, 500)
            await gold_page.keyboard.type("5")
            await asyncio.sleep(0.5)
            await gold_page.keyboard.press("Enter")
            await asyncio.sleep(2)

            screenshot_path = CHARTS_DIR / "active_gold_5m.png"
            await gold_page.screenshot(path=str(screenshot_path))

            title = await gold_page.title()
            print(f"SUCCESS: Screenshot saved to {screenshot_path}")
            print(f"LIVE PRICE (Title): {title.encode('ascii', 'ignore').decode('ascii')}")

            history_path = TMP_DIR / "price_history.txt"
            with history_path.open("a", encoding="utf-8") as handle:
                handle.write(f"{datetime.now().isoformat()},{title}\n")
        except Exception as exc:
            print(f"MONITOR ERROR: {exc}")


if __name__ == "__main__":
    asyncio.run(monitor_gold())
