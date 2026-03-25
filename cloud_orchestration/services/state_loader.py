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
        Reads all institutional docs and ledger state.
        """
        state = {"last_ledger_entry": {}, "phase": "UNKNOWN", "docs": {}}
        
        # List of all institutional files to ingest
        core_files = {
            "roadmap": "antigravity-institutional-roadmap.md",
            "ledger": "ANTIGRAVITY_v5.0_SOVEREIGN_LEDGER.csv",
            "schedule": "month_1_operational_schedule.md",
            "framework": "unified_operational_framework_v5.0.md",
            "summary": "analytical-session-summary.md",
            "protocol": "INSTITUTIONAL_WORK_PROTOCOL_v5.0.md"
        }
        
        docs_content = {}
        for key, filename in core_files.items():
            path = os.path.join(self.knowledge_dir, filename)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    docs_content[key] = f.read()
            else:
                docs_content[key] = f"File {filename} not found."

        state["docs"] = docs_content
        
        # Extract last ledger entry
        ledger_path = os.path.join(self.knowledge_dir, "ANTIGRAVITY_v5.0_SOVEREIGN_LEDGER.csv")
        if os.path.exists(ledger_path):
            with open(ledger_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                if rows:
                    state["last_ledger_entry"] = rows[-1]

        # Heuristic for phase extraction
        roadmap = docs_content.get("roadmap", "")
        if "PHASE 5" in roadmap.upper():
            state["phase"] = "Phase 5: Moonshot Stage"
        elif "PHASE 1" in roadmap.upper():
            state["phase"] = "Phase 1: Foundation"
        else:
            # Try to find the word 'Phase' followed by a number
            import re
            match = re.search(r'Phase\s*\d+', roadmap, re.IGNORECASE)
            if match:
                state["phase"] = match.group(0)
            else:
                state["phase"] = "Sovereign Operations"
            
        return state
