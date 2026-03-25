from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from playwright.async_api import async_playwright


ROOT_DIR = Path(__file__).resolve().parents[1]
CHART_DIR = ROOT_DIR / "charts"
sys.path.append(str(ROOT_DIR))

from find_cdp import find_cdp_endpoint


async def connect_and_capture(task_list: list[dict[str, object]]) -> None:
    cdp_endpoint = os.getenv("CDP_ENDPOINT") or find_cdp_endpoint() or "http://127.0.0.1:9222"

    async with async_playwright() as playwright:
        try:
            print(f"Connecting to browser at {cdp_endpoint}...")
            browser = await playwright.chromium.connect_over_cdp(cdp_endpoint)
            if not browser or not browser.contexts:
                print("Error: Could not connect to browser or no contexts found.")
                return

            context = browser.contexts[0]
            page = None
            for candidate in context.pages:
                try:
                    if "tradingview.com" in candidate.url:
                        page = candidate
                        break
                except Exception:
                    continue

            if not page:
                print("Error: No active TradingView tab found. Analysis halted.")
                return

            print(f"Session Sync: {page.url}")
            await page.bring_to_front()

            for task in task_list:
                symbol = str(task["symbol"])
                timeframes = task["tfs"]
                prefix = str(task["prefix"])

                await page.keyboard.press("Escape")
                await page.mouse.click(800, 500)
                await asyncio.sleep(1)
                await page.keyboard.type(symbol, delay=100)
                await page.keyboard.press("Enter")
                await asyncio.sleep(10)

                for timeframe in timeframes:
                    tf_cmd = "1D" if str(timeframe).upper() == "D" else str(timeframe)
                    filename_tf = "1d" if tf_cmd == "1D" else f"{tf_cmd}m"
                    print(f"Capturing {symbol} [{filename_tf}]...")

                    await page.keyboard.press("Escape")
                    await page.mouse.click(800, 500)
                    await page.keyboard.type(tf_cmd, delay=100)
                    await page.keyboard.press("Enter")
                    await asyncio.sleep(8)

                    save_path = CHART_DIR / f"{prefix}_{filename_tf}.png"
                    await page.screenshot(path=str(save_path))
                    print(f"Saved: {save_path}")
        except Exception as exc:
            print(f"Capture engine failure: {exc}")
        finally:
            print("--- MISSION COMPLETE ---")


async def main() -> None:
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    tasks = [
        {
            "symbol": "OANDA:XAUUSD",
            "tfs": ["1", "5", "15", "60", "240", "D"],
            "prefix": "gold_multipane",
        }
    ]
    await connect_and_capture(tasks)


if __name__ == "__main__":
    asyncio.run(main())
