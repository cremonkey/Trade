from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
TMP_DIR = ROOT_DIR / "tmp"
SKILL_SCRIPTS_DIR = ROOT_DIR / ".agents" / "skills" / "trade-twelve-data-feed" / "scripts"
sys.path.append(str(SKILL_SCRIPTS_DIR))

import twelve_data_client


def log_event(message: str) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def main() -> None:
    try:
        TMP_DIR.mkdir(parents=True, exist_ok=True)
        log_event("Starting Twelve Data Analysis Cycle...")
        data = twelve_data_client.full_analysis_cycle()

        # Integration Hardening: Add DXY calculation for dashboard
        try:
            from dxy_calculator import get_live_dxy
            log_event("Recalculating DXY Unit Weight...")
            data["dxy"] = get_live_dxy()
        except Exception as e:
            log_event(f"WARNING: DXY calculation failed: {e}")
            data["dxy"] = "N/A"


        scan_file = TMP_DIR / "scan_results.json"
        with scan_file.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)

        xau_price = data.get("prices", {}).get("XAU/USD", {}).get("price", "N/A")
        log_event(f"SUCCESS: Market data updated. XAU/USD: {xau_price}")
    except Exception as exc:
        log_event(f"FAILED: Twelve Data scan failed: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
