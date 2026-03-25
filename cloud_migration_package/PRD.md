# 🏛️ PRD: Antigravity Sovereign Cloud (v5.0)

## 1. Executive Summary
The goal is to migrate the local Antigravity v5.0 trading infrastructure to a 24/7 autonomous cloud-hosted system. The system must maintain institutional-grade data integrity, risk management (Institutional Unit Model), and provide a real-time interactive interface via a chatbot.

## 2. Terminology & Core Rules
- **Sovereign Grade**: 24/7 uptime with automated fundamental-technical verification.
- **Unit Model**: 0.01 lot size per $100 equity.
- **Lot Cap**: Absolute maximum of 5.00 lots.
- **OPEX Deduction**: Automated daily margin extraction for server costs.
- **FTCS**: Fundamental-Technical Convergence Score.

## 3. Functional Requirements
### 3.1 Automated Market Intelligence
- **Interval**: 15-minute high-frequency analysis cycle.
- **Data**: Fetch live XAU/USD, DXY, and XAG/USD via Twelve Data API.
- **Logging**: Maintain a persistent `trading_journal` and `session_summaries` in a database.

### 3.2 Alert & Command System
- **Real-Time Alarms**: Instant PUSH notifications to the user's phone (Telegram) when targets are hit.
- **Interactive Chat**: Support for commands: `/status`, `/audit`, `/plan`, `/execute`.
- **Roadmap Persistence**: Track the "Phase 5 Moonshot" progress automatically.

### 3.3 Security & Compliance
- **Safe-Halt**: Automatic 24h Discipline Lock if a manual rule breach is detected.
- **Encrypted Keys**: API keys stored in environment variables (never in code).

## 4. Technical Stack (Recommended)
- **Backend**: Python (FastAPI).
- **Automation**: GitHub Actions or VPS Crontab.
- **Persistence**: Supabase (PostgreSQL).
- **Frontend**: Telegram Bot API / Vercel AI SDK.

---
*Status: READY FOR IMPLEMENTATION*
