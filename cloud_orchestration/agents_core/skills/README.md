# GoldEdge Modular Trading Skills

This directory contains the specialized support skills behind the Antigravity v4.4 XAU/USD workflow.
The root-level v4.4 operating documents remain the source of truth whenever a skill conflicts with them.

## Skills Overview

1. **[trade-goldedge-analyst](./trade-goldedge-analyst/SKILL.md)**: The orchestrator and summary layer.
2. **[trade-liquidity-mapper](./trade-liquidity-mapper/SKILL.md)**: HTF structure, order blocks, and liquidity zones.
3. **[trade-execution-specialist](./trade-execution-specialist/SKILL.md)**: Precision entry and exit logic after risk and timing are green.
4. **[trade-risk-manager](./trade-risk-manager/SKILL.md)**: Capital preservation, ATR gating, and lock awareness.
5. **[trade-session-strategist](./trade-session-strategist/SKILL.md)**: Session timing behavior and approved windows.
6. **[trade-macro-researcher](./trade-macro-researcher/SKILL.md)**: HTF targets, yields, and cross-asset macro context.
7. **[trade-news-radar](./trade-news-radar/SKILL.md)**: Real-time news and sentiment monitoring.
8. **[trade-regime-architect](./trade-regime-architect/SKILL.md)**: Market regime and range nesting.
9. **[trade-twelve-data-feed](./trade-twelve-data-feed/SKILL.md)**: Live price acquisition and supporting correlation inputs.
10. **[trade-weekly-market-architect](./trade-weekly-market-architect/SKILL.md)**: Weekly structure and HTF liquidity profiles.
11. **[trade-weekly-economic-planner](./trade-weekly-economic-planner/SKILL.md)**: Weekly macro-event landscape and volatility clusters.

## Workflow

1. Timing: Consult `trade-session-strategist` to confirm the current window is valid under v4.4.
2. Context: Use `trade-liquidity-mapper` to define bias and key zones.
3. Safety: Use `trade-risk-manager` to validate volatility, lock status, and sizing.
4. Execution: Use `trade-execution-specialist` only after timing and safety are green.
5. Reporting: Use `trade-goldedge-analyst` to summarize the result while cross-checking the root roadmap and brief.
