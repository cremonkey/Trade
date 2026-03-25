import os
import csv
from typing import Dict, Any, List

class StateLoader:
    """
    Directly loads the Sovereign Ledger and Institutional Roadmap as the source of truth.
    """
    
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.knowledge_dir = os.path.join(self.base_path, "knowledge")

    def get_sovereign_state(self) -> Dict[str, Any]:
        """
        Reads the CSV ledger and MD roadmap.
        """
        state = {
            "last_ledger_entry": {},
            "institutional_roadmap": "",
            "phase": "UNKNOWN"
        }
        
        # 1. Load Ledger
        ledger_path = os.path.join(self.knowledge_dir, "ANTIGRAVITY_v5.0_SOVEREIGN_LEDGER.csv")
        if os.path.exists(ledger_path):
            with open(ledger_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                if rows:
                    state["last_ledger_entry"] = rows[-1]

        # 2. Load Roadmap
        roadmap_path = os.path.join(self.knowledge_dir, "antigravity-institutional-roadmap.md")
        if os.path.exists(roadmap_path):
            with open(roadmap_path, 'r', encoding='utf-8') as f:
                content = f.read()
                state["institutional_roadmap"] = content
                # Extract Phase (Simple heuristic)
                if "PHASE 1" in content.upper() and "[x]" not in content:
                    state["phase"] = "PHASE 1: THE FOUNDATION"
                elif "PHASE 2" in content.upper():
                    state["phase"] = "PHASE 2: THE SOVEREIGN MOONSHOT"

        return state
