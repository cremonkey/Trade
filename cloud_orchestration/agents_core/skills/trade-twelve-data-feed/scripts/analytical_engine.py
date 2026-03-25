from __future__ import annotations

import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(__file__).resolve().parents[4]
sys.path.append(str(SCRIPT_DIR))

import liquidity_analyzer
import dxy_calculator
import twelve_data_client


def build_smt_context(data: dict) -> tuple[str, str]:
    xag_payload = data.get("prices", {}).get("XAG/USD", {})
    if xag_payload.get("price"):
        return f"XAG/USD active: {xag_payload['price']}", "direct"

    try:
        slv_data = twelve_data_client.td_get("price", {"symbol": "SLV", "dp": 4})
        slv_price = slv_data.get("price", "N/A")
        return f"SLV fallback active: {slv_price}", "fallback"
    except Exception:
        message = xag_payload.get("message", "No SMT companion price available.")
        return f"SMT limited: {message}", "limited"


def generate_report(data_file: str | Path) -> str:
    data_path = Path(data_file)
    with data_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    daily_candles = data.get("daily", {}).get("values", [])
    ipda = liquidity_analyzer.calculate_ipda_ranges(daily_candles)

    atr = data.get("atr", {}).get("values", [{}])[0].get("atr", "0")
    rsi = data.get("rsi", {}).get("values", [{}])[0].get("rsi", "0")
    regime = liquidity_analyzer.analyze_volatility(atr)

    m15_candles = data.get("m15", {}).get("values", [])
    fvgs = liquidity_analyzer.detect_fvgs(m15_candles)
    recent_fvgs = fvgs[-5:]

    xau = data.get("prices", {}).get("XAU/USD", {}).get("price", "N/A")
    dxy = dxy_calculator.get_live_dxy()
    smt_status, smt_mode = build_smt_context(data)

    report = f"""
# Antigravity v4.4 Institutional Market Report
**Time (UTC)**: {data.get('timestamp', 'N/A')}

---

## SECTION 1: REGIME AND CORRELATION
* **Current Price (XAU/USD)**: **{xau}**
* **Synthetic DXY Index**: **{dxy}**
* **SMT Context**: **{smt_status}**
* **SMT Mode**: **{smt_mode}**
* **Volatility Mode**: **{regime}** (ATR 5m: {atr})
* **Momentum (RSI 1h)**: {rsi}

---

## SECTION 2: IPDA LIQUIDITY ARCHITECTURE
| Threshold | High | Low | Equilibrium |
|-----------|------|-----|-------------|
| IPDA 20 | {ipda['ipda20']['high']} | {ipda['ipda20']['low']} | {ipda['ipda20']['eq']} |
| IPDA 40 | {ipda['ipda40']['high']} | {ipda['ipda40']['low']} | {ipda['ipda40']['eq']} |
| IPDA 60 | {ipda['ipda60']['high']} | {ipda['ipda60']['low']} | {ipda['ipda60']['eq']} |

---

## SECTION 3: RECENT FAIR VALUE GAPS
"""

    for fvg in recent_fvgs:
        report += (
            f"- [{fvg['type']}] {fvg['datetime']} | "
            f"Range: {fvg['bottom']} - {fvg['top']} | CE: {fvg['ce']}\n"
        )

    report += """

---

Use the root v4.4 roadmap and brief before converting this report into execution.
"""
    return report


if __name__ == "__main__":
    report_md = generate_report(ROOT_DIR / "tmp" / "scan_results.json")
    output_path = ROOT_DIR / "tmp" / "report.md"
    output_path.write_text(report_md, encoding="utf-8")
    print(f"Report generated: {output_path}")
