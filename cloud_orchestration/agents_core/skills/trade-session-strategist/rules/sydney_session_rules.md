# SYDNEY OPEN PROTOCOL (v4.4)

## WINDOW: 00:00 - 02:00 UTC+2

### CORE OBJECTIVE
Monitor spread expansion and stop-run behavior around the open. This is primarily an observation window, not a preferred execution window.

## CONTEXT
1. Note previous day high and low.
2. Observe the first 30 minutes for a sweep and snapback.
3. Treat early expansion as informational unless the root framework explicitly authorizes action.

## RISK MANAGEMENT
* **Lot Size**: **0.01 ONLY**.
* **Timing Rule**: Never enter before 00:30 UTC+2.
* **Spread Rule**: If spread is > 5 points, stay out.

## DATA CHECK
* **Gap Risk**: Compare current price to yesterday's close.
* **ATR(5m)**: If > 10.0, treat the session as execution-halt territory for scalp logic.
