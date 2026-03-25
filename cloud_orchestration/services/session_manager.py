import os
from datetime import datetime
from typing import Dict, Any

class SessionManager:
    """
    Identifies the active trading session and loads corresponding rules.
    Ported from Antigravity v4.4 Session Navigator.
    """
    
    def get_current_session(self, current_time: datetime) -> str:
        hour = current_time.hour
        minute = current_time.minute
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

    def get_session_rules(self, session: str) -> str:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rules_dir = os.path.join(base_path, "agents_core", "skills", "trade-session-strategist", "rules")
        
        mapping = {
            "SYDNEY_OPEN": "sydney_session_rules.md",
            "ASIAN_SESSION": "asian_session_rules.md",
            "LONDON_MORNING": "london_morning_rules.md",
            "NEW_YORK_KILL_ZONE": "ny_session_rules.md",
        }
        
        rule_file = mapping.get(session)
        if not rule_file:
            return "No specific rules found for this session context."
            
        full_path = os.path.join(rules_dir, rule_file)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        return f"Rule file {rule_file} not found in {rules_dir}."
