# SKILL: GoldEdge Risk Manager (v5.0)

## Description
Capital-preservation layer for XAU/USD. Use this skill to validate volatility, lock status, and allowable sizing based on the **Institutional Unit Model**.

## Instructions
1. Use the **Unit Model**: **0.01 lot per $100** of equity until $1,000. Above $1,000, use **0.10 lot per $1,000**.
2. **Absolute Cap**: Never exceed **5.00 lots** regardless of equity, to prevent slippage and liquidity risk.
3. **OPEX Consciousness**: All trades must account for a **Daily Operational Margin** ($5 - $30) before net compounding is recorded.
4. **Discipline Lock**: 24h lockout remains mandatory after 2 losses or a confirmed protocol violation.
5. **Volatility Filter**: Halt execution if M5 ATR is above 10.0 gold points.
6. **Triple Lock**: IPDA Alignment + Structural Shift + SMT Confirmation must be present for any high-lot (>0.10) entries.

