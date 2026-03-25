from __future__ import annotations

import os
import sys
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from find_cdp import find_cdp_endpoint


async def get_price() -> None:
    cdp_endpoint = os.getenv("CDP_ENDPOINT") or find_cdp_endpoint() or "http://127.0.0.1:9222"

    async with async_playwright() as playwright:
        try:
            browser = await playwright.chromium.connect_over_cdp(cdp_endpoint)
            if not browser or not browser.contexts:
                print("Error: Browser context not reachable.")
                return

            pages = browser.contexts[0].pages
            page = None
            for candidate in pages:
                try:
                    title = await candidate.title()
                    if title and ("XAUUSD" in title.upper() or "GOLD" in title.upper()):
                        page = candidate
                        break
                except Exception:
                    continue

            page = page or (pages[0] if pages else None)
            if not page:
                print("Error: No pages accessible in context.")
                return

            title = await page.title()
            clean_title = title.encode("ascii", "ignore").decode("ascii")
            print(f"TV HEARTBEAT: {clean_title}")
        except Exception as exc:
            print(f"Heartbeat Failure: {exc}")


if __name__ == "__main__":
    asyncio.run(get_price())
