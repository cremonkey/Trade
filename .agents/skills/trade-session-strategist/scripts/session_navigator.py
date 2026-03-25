from __future__ import annotations

from datetime import datetime
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[4]
RULES_PATH = Path(__file__).resolve().parents[1] / "rules"


def get_current_session(time_local: datetime) -> str:
    """
    Identifies the active trading context using the project operating timezone.
    """
    hour = time_local.hour
    minute = time_local.minute
    total_minutes = hour * 60 + minute

    if 0 <= total_minutes < 120:
        return "SYDNEY_OPEN"
    if 120 <= total_minutes < 420:
        return "ASIAN_SESSION"
    if 420 <= total_minutes < 660:
        return "LONDON_MORNING"
    if 660 <= total_minutes < 870:
        return "MIDDAY_TRANSITION"
    if 870 <= total_minutes < 1020:
        return "NEW_YORK_KILL_ZONE"
    if 1020 <= total_minutes < 1320:
        return "NEW_YORK_AFTERNOON"
    return "MARKET_CLOSE_GAP"


def get_rules_file(session: str) -> Path | None:
    mapping = {
        "SYDNEY_OPEN": RULES_PATH / "sydney_session_rules.md",
        "ASIAN_SESSION": RULES_PATH / "asian_session_rules.md",
        "LONDON_MORNING": RULES_PATH / "london_morning_rules.md",
        "NEW_YORK_KILL_ZONE": RULES_PATH / "ny_session_rules.md",
    }
    return mapping.get(session)


def main() -> None:
    now = datetime.now()
    session = get_current_session(now)

    print("--- ANTIGRAVITY v4.4 SESSION NAVIGATOR ---")
    print(f"Current System Time: {now.strftime('%H:%M:%S')}")
    print(f"Active Market Context: {session}")
    print("-" * 40)

    rules_file = get_rules_file(session)
    if rules_file and rules_file.exists():
        print("\nACTIVE RULES & PROTOCOL:")
        print(rules_file.read_text(encoding="utf-8"))
    else:
        print("\nNo dedicated rule file for this session window.")
        print("Fallback: Use root v4.4 roadmap and framework.")


if __name__ == "__main__":
    main()
