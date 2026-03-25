# SKILL: GoldEdge News Radar & Sentiment Processor (Layer 9)

## Description
Real-time news wire processing and sentiment analysis engine for XAU/USD.

## Instructions
1.  **News Source Hierarchy**:
    *   Tier 1: Reuters, Bloomberg, BLS, Fed.
    *   Tier 2: FT, WSJ, CNBC, ForexFactory.
    *   Tier 3: TradingView, verified X accounts.
2.  **Economic Calendar Integration**:
    *   Identify Critical (RED), High (ORANGE), and Medium (YELLOW) impact events.
    *   **RED Window**: No entries 15m before. Close or hedge existing positions.
    *   **Clustered Event Rule**: Treat windows with 2+ ORANGE events as RED.
3.  **Sentiment Scoring (GSS)**:
    *   Produce **Gold Sentiment Score (-100 to +100)**.
    *   **Extreme Sentiment (±70)**: Issue "Crowded Trade Alert." Prioritize counter-sentiment liquidity sweeps.
4.  **Breaking News Impact (BNIC)**:
    *   Classify headlines: **C1** (Halt all), **C2** (Pause entries), **C3** (No change).
    *   Speed mandate: Process headlines within 60 seconds.
