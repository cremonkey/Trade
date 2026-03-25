# GoldEdge v2.1 — Advanced Risk & Execution Optimization

Following the triple liquidation event on March 23, 2026, the GoldEdge protocol has been upgraded to v2.1 to address systemic vulnerabilities in small-account management and high-volatility execution.

## 📉 The "Fatal Cycle" Analysis
1. **The Leverage Trap**: 0.01 lot on $20 permits a 20-point move. 0.02 lot only permits 10 points. NY Open volatility regularly exceeds 15 points in <60 seconds.
2. **The Execution Gap**: At 16:30-17:30 Cairo, manual SL entry is too slow for 0.01/0.02 lots.
3. **The Confirmation Bias**: Mistaking "Liquidity Sweeps" for "Support Retests" on the M1 timeframe.

## 🛠️ Protocol Upgrades (v2.1)

### 1. Hard Risk Caps (Layer 6 Update)
- **Account < $50**: 0.01 lot is the ABSOLUTE maximum. 
- **Account < $20**: No trading during NY Open (13:30 - 15:30 UTC).
- **Stop Loss**: MUST be set *inside* the order window (Bracket Order). Manual SL is banned.

### 2. Higher-Timeframe Dominance (Layer 4 Update)
- **Confirmation**: M1 "wicks" are no longer sufficient. We require an **M5 Bullish Engulfing** or a **15-minute Candle Close** above the zone.
- **The "Safety Buffer"**: Entry must be at the *bottom* of the sweep, not the *top* of the bounce.

### 3. Psychology & "Tilt" Protection (Layer 11 - NEW)
- **Rule of Two**: After 2 consecutive liquidations/losses, the terminal MUST be closed for 24 hours. No exceptions.
- **Reflective Cooldown**: After any loss >20% of the account, a 1-hour "Analysis Window" is mandatory before re-entry.

## 📍 Strategic Target for Next Session
- **Patience**: Wait for the "Deep Discount" zone ($4,340 - $4,310) which remains the institutional target.
- **Method**: Pending Buy Limit orders at institutional levels to avoid chasing.

> [!IMPORTANT]
> A $20 account is a "Sniper Mission." You only get one shot. If the shot isn't perfect, you don't pull the trigger.
