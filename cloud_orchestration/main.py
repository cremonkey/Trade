import os
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

from services.risk_manager import RiskManager
from services.execution import ExecutionSpecialist
from services.news_analyst import NewsAnalyst
from services.gemini_intelligence import GeminiIntelligence
from integrations.supabase_client import SupabaseIntegration
from integrations.telegram_bot import TelegramIntegration
from integrations.twelve_data import TwelveDataIntegration
from services.session_manager import SessionManager
from services.state_loader import StateLoader

app = FastAPI(title="Antigravity Sovereign Cloud")

# Initialize components
risk_manager = RiskManager()
execution = ExecutionSpecialist()
news_analyst = NewsAnalyst()
brain = GeminiIntelligence()
supabase = SupabaseIntegration()
telegram = TelegramIntegration()
twelve_data = TwelveDataIntegration()
session_manager = SessionManager()
state_loader = StateLoader()

class AnalysisResult(BaseModel):
    timestamp: str
    symbol: str
    price: float
    lot_size: float
    ftcs_score: int
    status: str

@app.get("/")
def read_root():
    return {"status": "online", "system": "Antigravity Sovereign Cloud v5.0"}

@app.get("/status")
async def get_status():
    """
    Returns a consolidated Markdown brief.
    """
    try:
        config = supabase.get_system_config()
        is_locked = risk_manager.is_discipline_locked(config.get("discipline_lock_until"))
        
        status_data = {
            "balance": config.get("balance"),
            "equity": config.get("equity"),
            "lot_size": risk_manager.calculate_lot_size(config.get("equity")),
            "phase": config.get("phase"),
            "is_locked": is_locked
        }
        
        report = telegram.format_status_report(status_data)
        return {"report": report, "data": status_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analyze")
async def trigger_analysis(background_tasks: BackgroundTasks):
    """
    Triggers the full 5-script analysis suite.
    """
    background_tasks.add_task(run_analysis_cycle)
    return {"message": "Analysis cycle started in background"}

async def run_analysis_cycle():
    """
    The 15-minute analysis logic.
    """
    print(f"[{datetime.now()}] Starting analysis cycle...")
    
    # 1. Load Institutional State (Roadmap & Ledger)
    sovereign_state = state_loader.get_sovereign_state()
    current_session = session_manager.get_current_session(datetime.now())
    session_rules = session_manager.get_session_rules(current_session)
    
    # 2. Fetch market data
    prices = await twelve_data.get_market_data()
    gold_price = prices.get("XAU/USD")
    print(f"[{datetime.now()}] Session: {current_session} | Market Data: {prices}")
    
    # 3. Check risk & config
    try:
        config = supabase.get_system_config()
    except Exception as e:
        print(f"[{datetime.now()}] Supabase Error: {e}")
        return

    equity = config.get("equity", 88.00)
    lot_size = risk_manager.calculate_lot_size(equity)
    
    # 4. AI Brain Analysis (Directly from Roadmap/Ledger)
    analysis_context = {
        "prices": prices,
        "ledger": sovereign_state.get("last_ledger_entry"),
        "roadmap_phase": sovereign_state.get("phase"),
        "session": current_session,
        "session_rules": session_rules
    }
    
    ai_decision = await brain.analyze_market(analysis_context, "N/A")
    print(f"[{datetime.now()}] Institutional Decision: {ai_decision}")
    
    # 5. Push Alerts (Arabic & Detailed)
    if gold_price:
        status_emoji = "🛡️ تنفيذ سيادي (EXECUTE)" if ai_decision.get("execute") else "⏳ مراقبة (MONITORING)"
        sent = await telegram.send_alert(
            f"🏛️ **القرار المؤسسي**: {status_emoji}\n"
            f"--- \n"
            f"📈 المرحلة: {sovereign_state.get('phase')}\n"
            f"🌍 الجلسة: {current_session}\n"
            f"💰 سعر الذهب مباشر: ${gold_price}\n"
            f"🎯 الاتجاه: {ai_decision.get('bias', 'NEUTRAL')}\n"
            f"⚖️ تقييم التقارب (FTCS): {ai_decision.get('ftcs_score', 0)}\n"
            f"\n📜 **التحليل التفصيلي**:\n{ai_decision.get('reasoning', 'N/A')}"
        )
        print(f"[{datetime.now()}] Telegram Alert Sent: {sent}")
    else:
        print(f"[{datetime.now()}] Skipping Telegram Alert: No Gold Price found.")
    
    print(f"[{datetime.now()}] Analysis cycle completed.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
