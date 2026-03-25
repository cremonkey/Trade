# SKILL: GoldEdge Execution Specialist (v5.0)

## Description
Precision execution layer for XAU/USD. Use this skill only after timing, structure, and risk are already aligned.

## Instructions
1. **Pillar Lock**: Never authorize execution while a Discipline Lock is active.
2. **Phase Lock**: Confirm lot size matches the **Institutional Unit Model** (e.g. 0.01 per $100).
3. **Zone Lock**: Never authorize execution outside approved v5.0 kill zones (London AM / NY AM).
4. **Data Sync**: Confirm feed and browser are synchronized within **0.5 gold points**.
5. **Setup Validation**: Require a valid liquidity interaction + MSS/CHoCH + **SMT Divergence** before calling an entry executable.
6. **Execution Method**: Use **Sniper-style** no-chase execution. If the move leaves the OTE zone, let it go.
7. **Absolute Rule**: Do not exceed **5.00 lots** under any circumstances in the Sovereign phase.

