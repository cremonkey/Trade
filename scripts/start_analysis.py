from __future__ import annotations

import datetime
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def log_event(message: str) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def run_script(relative_path: str) -> bool:
    script_path = ROOT_DIR / relative_path
    log_event(f"Executing {script_path}...")
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            cwd=ROOT_DIR,
        )
    except Exception as exc:
        log_event(f"ERROR: {exc}")
        return False

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

    if result.returncode == 0:
        log_event(f"SUCCESS: {relative_path}")
        return True

    log_event(f"FAILED: {relative_path}")
    return False


def main() -> None:
    print("--- ANTIGRAVITY v5.0 MASTER ANALYSIS SUITE ---")
    targets = [
        "scripts/fetch_market_data.py",  # Primary API Data
        "scripts/quick_price.py",       # CDP Heartbeat
        "scripts/monitor_active.py",     # Active Gold Snapshot
        "scripts/chart_scout.py",        # Multi-TF Chart Audit
    ]
    results = {target: run_script(target) for target in targets}

    print("\n--- FUNDAMENTAL NEWS CHECK ---")
    news_path = ROOT_DIR / "fundamental_context.md"
    if news_path.exists():
        log_event("NEWS STATUS: fundamental_context.md FOUND. Audit active.")
    else:
        log_event("NEWS WARNING: fundamental_context.md MISSING. High risk of news-spike.")

    print("\n--- INSTITUTIONAL v5.0 SOVEREIGNTY CHECK ---")

    # v5.0 Hardening: Verify Roadmap Readiness
    try:
        roadmap_path = ROOT_DIR / "antigravity-institutional-roadmap.md"
        with open(roadmap_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if "READY FOR DAY 1 START" in content:
                log_event("V5.0 ADHERENCE: Roadmap is in Execution Mode.")
            else:
                log_event("V5.0 WARNING: Roadmap is not yet set to 'READY'.")
    except Exception as e:
        log_event(f"V5.0 CHECK FAILED: {e}")

    print("\n--- ANALYSIS CYCLE COMPLETE ---")
    all_ok = all(results.values())
    for target, success in results.items():
        print(f"{target}: {'OK' if success else 'FAILED'}")
    
    if all_ok:
        log_event("SYSTEM STATUS: SOVEREIGN GRADE READINESS CONFIRMED.")
    else:
        log_event("SYSTEM STATUS: PARTIAL SUITE FAILURE (Check Logs).")




if __name__ == "__main__":
    main()
