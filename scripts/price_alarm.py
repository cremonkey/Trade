from __future__ import annotations

import time
import ctypes
import json
import sys
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

# Ensure Twelve Data Client is in path
SKILL_SCRIPTS_DIR = ROOT_DIR / ".agents" / "skills" / "trade-twelve-data-feed" / "scripts"
sys.path.append(str(SKILL_SCRIPTS_DIR))

try:
    import twelve_data_client
except ImportError:
    print("Error: twelve_data_client not found. Ensure .agents/skills is intact.")
    sys.exit(1)

def play_alert(price, target):
    """Triggers a Windows Message Box alert."""
    message = f"🚨 ANTIGRAVITY ALARM TRIGGERED 🚨\n\nTarget: {target}\nCurrent Price: {price}\n\nAction: SEND 'START' TO SESSION CHAT NOW."
    # 0x40 = Icon Information, 0x1 = OK/Cancel, 0x1000 = System Modal (Always on top)
    ctypes.windll.user32.MessageBoxW(0, message, "v5.0 Institutional Alarm", 0x40 | 0x1 | 0x1000)

def get_current_price():
    try:
        # Correctly call the td_get method from the client
        data = twelve_data_client.td_get("price", {"symbol": "XAU/USD"})
        return float(data.get("price", 0))
    except Exception as e:
        print(f"Fetch Error: {e}")
        return None


def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/price_alarm.py <target_price> <direction: above/below>")
        return

    target = float(sys.argv[1])
    direction = sys.argv[2].lower()
    
    print(f"--- ANTIGRAVITY ALARM ACTIVE ---")
    print(f"Monitoring XAU/USD for price to go {direction} {target}...")

    while True:
        price = get_current_price()
        if price:
            print(f"[{time.strftime('%H:%M:%S')}] XAU/USD: {price:.4f} (Target: {target})", end="\r")
            
            triggered = False
            if direction == "above" and price >= target:
                triggered = True
            elif direction == "below" and price <= target:
                triggered = True

            if triggered:
                print(f"\n\n[!!!] TARGET REACHED: {price}")
                # Create a trigger file for the agent to see
                trigger_path = ROOT_DIR / "tmp" / "ALARM_TRIGGERED.txt"
                with open(trigger_path, "w") as f:
                    f.write(f"ALARM TRIGGERED AT {time.strftime('%H:%M:%S')} | PRICE: {price} | TARGET: {target}")
                
                play_alert(price, target)
                break
        
        time.sleep(10) # Poll every 10 seconds (Within typical API limits)

if __name__ == "__main__":
    main()
