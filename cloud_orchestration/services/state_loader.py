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
        # Heuristic for phase extraction
        roadmap = docs_content.get("roadmap", "")
        if "PHASE 1" in roadmap.upper() and "[x]" not in roadmap:
            state["phase"] = "PHASE 1 (Foundation)"
        elif "PHASE 2" in roadmap.upper():
            state["phase"] = "PHASE 2 (Moonshot)"
            
        return state
