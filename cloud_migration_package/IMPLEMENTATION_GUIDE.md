# 🛠️ IMPLEMENTATION GUIDE: Cloud Migration

## Targeted Architecture
We are building a **Serverless-Ready** Python backend that orchestrates the existing Antigravity v5.0 logic.

## Step-by-Step Blueprint

### Step 1: Framework Scaffolding
- Initialize a FastAPI project.
- Create an `/analyze` endpoint that triggers the consolidated `start_analysis.py` logic.
- Port over the `.agents/skills` logic into a `services/` package.

### Step 2: Persistence Setup (Supabase)
- Create a `trading_history` table for the journal.
- Create a `system_config` table to store the current `Balance`, `Lot_Size`, and `Phase`.
- Replace local CSV/Markdown writing with API-based upserts.

### Step 3: Telegram Integration
- Initialize a `python-telegram-bot`.
- Implement a `send_alert()` function triggered by the `price_alarm.py` logic.
- Map commands:
  - `/status` -> Returns the latest Master Intelligence Brief.
  - `/analyze` -> Triggers the full 5-script analysis suite.

### Step 4: Deployment & Cron
- Deploy to a VPS or Vercel.
- Configure a 15-minute cron job to call the `/analyze` endpoint.
- Verify DXY calculation and Twelve Data rate-limit handling in the hosted environment.

## 🚨 Critical Constraints
- **Do NOT touch the local files**: All work must happen in the `cloud_orchestration/` or a separate repo.
- **Preserve the v5.0 Rules**: $88 starting balance, 0.01 lot per $100, 5-lot cap.
