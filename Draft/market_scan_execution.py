import sys
import os
import json

# Add scripts directory to path
sys.path.append(os.path.abspath(r"c:\Users\atmom\OneDrive\Desktop\Trade\.agents\skills\trade-twelve-data-feed\scripts"))

import twelve_data_client

def main():
    try:
        print("Starting Twelve Data Analysis Cycle (8 credits)...")
        data = twelve_data_client.full_analysis_cycle()
        
        # Save to a temporary JSON file for the AI to read
        with open("tmp/scan_results.json", "w") as f:
            json.dump(data, f, indent=2)
        
        print("Scan completed successfully. Results saved to tmp/scan_results.json.")
        
        # Print a quick summary for immediate feedback
        print(f"\nQuick Summary:")
        print(f"XAU/USD Price: {data['prices'].get('XAU/USD', {}).get('price')}")
        print(f"XAG/USD Price: {data['prices'].get('XAG/USD', {}).get('price')}")
        print(f"ATR (5m): {data['atr'].get('values', [{}])[0].get('atr')}")
        print(f"RSI (1h): {data['rsi'].get('values', [{}])[0].get('rsi')}")
        
    except Exception as e:
        print(f"Scan failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
