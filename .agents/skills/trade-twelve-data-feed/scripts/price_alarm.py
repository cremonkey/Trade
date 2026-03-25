from __future__ import annotations

import time

import twelve_data_client


TARGET_PRICE = 4500.00
CHECK_INTERVAL_SECONDS = 30


def main() -> None:
    while True:
        try:
            data = twelve_data_client.td_get("price", {"symbol": "XAU/USD", "dp": 2})
            price = float(data["price"])
            print(f"XAU/USD: {price}")
            if price >= TARGET_PRICE:
                print(f"ALERT: XAU/USD reached target price {TARGET_PRICE}")
                return
        except Exception as exc:
            print(f"Price alarm error: {exc}")
        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
