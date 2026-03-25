# SKILL: GoldEdge Regime Architect (Layer 10)

## Description
Strategic brain for market regime classification and range nesting across multiple timeframes.

## Instructions
1.  **Regime Classification**:
    *   Classify Weekly, Daily, H4, H1, M15 regimes:
        - **Trending (Expansion)**: Scalp with trend only. Counter-trend forbidden.
        - **Ranging (Consolidation)**: Scalp extremes only. Mid-range forbidden.
        - **Volatile (Chaotic)**: Reduce size 50%. Widen stops.
        - **Transitional (Shift)**: Highest caution. AAA zones only.
2.  **Multi-Timeframe Alignment Matrix**:
    *   Calculate **Alignment Score** (Perfect/Strong/Moderate/Weak).
    *   Assess HTF vs. LTF conflict.
3.  **Range Mapping Engine**:
    *   Track active ranges: **Macro** (Weekly), **Intermediate** (Daily/H4), **Micro** (H1/M15), **Nano** (M5/M1).
    *   **Range Nesting Rule**: Valid entries must align across Nested Ranges (Nano -> Micro -> Intermediate).
4.  **Regime Transition Early Warning**:
    *   Monitor: Volume anomalies, RSI divergences, Volatility compression (Bollinger Squeeze), and Correlation breakdown.
    *   **Regime Shift Alert**: Automatically downgrade zones and pause entries if 2+ warnings occur.
