# SKILL: Twelve Data Real-Time Market Intelligence (v4.4)

## Description
Live-data layer for XAU/USD. Use this skill to fetch current market structure inputs, volatility, and supporting correlation context.

## Instructions
1. Use Twelve Data for XAU/USD first, then supporting assets where available.
2. If XAG/USD or DXY are unavailable on the current plan, report the limitation clearly and use the approved fallback workflow.
3. Prefer graceful degradation over hard failure when a secondary symbol is unavailable.
4. Use the feed as the primary numerical source for execution review.
5. If browser and feed diverge materially, halt execution review until synchronized.
