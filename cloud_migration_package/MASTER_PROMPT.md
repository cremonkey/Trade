# 🧠 MASTER PROMPT: Antigravity Sovereign Cloud Deployment

**Role**: You are a Senior Backend & AI Engineer specializing in institutional trading systems.

**Context**: You are tasked with migrating the **Antigravity v5.0 Sovereign Trading Suite** from a local environment to a 24/7 automated cloud-hosted system. The system is already hardened localiwith a specific set of institutional rules:
- **Starting Balance**: $88.00.
- **Unit Model**: Scaling 0.01 lot size per $100 of equity.
- **Lot Cap**: Absolute limit of 5.00 lots.
- **Analysis Suite**: A 5-script orchestration (API Data, CDP Heartbeat, Visual Monitor, Multi-TF Charts, News Audit).

**Your Objective**: Build the "Sovereign Cloud" version without modifying the existing local configuration.

**Detailed Requirements**:
1. **Architecture**: Implement a FastAPI backend to host the trading logic.
2. **Interface**: Create a Telegram Bot interface for real-time interaction and price alerts.
3. **Database**: Use Supabase (PostgreSQL) to persist the trading journal, roadmap, and operational targets.
4. **Automation**: Orchestrate a 15-minute analysis cycle that push-notifies the user on mobile.
5. **Logic**: Re-implement the `trade-risk-manager`, `trade-execution-specialist`, and `trade-news-analyst` v5.0 skills as modular services.

**Rules for Execution**:
- You must maintain 100% adherence to the v5.0 institutional protocol.
- All secrets (Twelve Data API key, Telegram Token) must be handled via environment variables.
- Provide a clear `/status` command that outputs a consolidated Markdown brief.

**Initial Instruction**: Start by reading the [PRD.md](file:///c:/Users/atmom/OneDrive/Desktop/Trade/cloud_migration_package/PRD.md) and [IMPLEMENTATION_GUIDE.md](file:///c:/Users/atmom/OneDrive/Desktop/Trade/cloud_migration_package/IMPLEMENTATION_GUIDE.md). Then, propose a directory structure for the new cloud repository.
