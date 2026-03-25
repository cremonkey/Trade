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
from integrations.yahoo_finance import YahooFinanceIntegration
from services.session_manager import SessionManager
from services.state_loader import StateLoader
from services.news_radar import NewsRadar

app = FastAPI(title="Antigravity Sovereign Cloud")

# Initialize components
risk_manager = RiskManager()
execution = ExecutionSpecialist()
news_analyst = NewsAnalyst()
brain = GeminiIntelligence()
supabase = SupabaseIntegration()
telegram = TelegramIntegration()
market_data = YahooFinanceIntegration()
session_manager = SessionManager()
state_loader = StateLoader()
news_radar = NewsRadar()

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

@app.post("/webhook/telegram")
async def telegram_webhook(update: dict, background_tasks: BackgroundTasks):
    """
    Handles incoming Telegram commands for on-demand analysis.
    """
    message = update.get("message", {})
    chat_id = str(message.get("chat", {}).get("id", ""))
    text = message.get("text", "").lower()
    
    # Security: Only allow the authorized user
    if chat_id != os.getenv("TELEGRAM_CHAT_ID"):
        return {"status": "unauthorized"}

    if "analyze" in text or "تحليل" in text:
        await telegram.send_alert("⚙️ **جاري بدء التحليل اللحظي بناءً على طلبك...**")
        background_tasks.add_task(run_analysis_cycle)
        return {"status": "triggered"}
    
    return {"status": "ignored"}

@app.get("/analyze")
async def trigger_analysis(background_tasks: BackgroundTasks):
    """
    Triggers the full 5-script analysis suite.
    """
    background_tasks.add_task(run_analysis_cycle)
    return {"message": "Analysis cycle started in background"}

async def run_analysis_cycle():
    """
    Enforces the 'Sequential Intelligence' Protocol (v5.1):
    1. Start Analysis (State Load)
    2. Vision Scan (Market Data Audit)
    3. News Radar (Fundamental Search)
    4. Sovereign Result (AI Brain)
    """
    print(f"[{datetime.now()}] --- PHASE 1: START ANALYSIS (Institutional Grade) ---")
    
    # 1. Start Analysis (Load Institutional State)
    sovereign_state = state_loader.get_sovereign_state()
    current_session = session_manager.get_current_session(datetime.now())
    session_rules = session_manager.get_session_rules(current_session)
    
    print(f"[{datetime.now()}] --- PHASE 2: VISION SCAN (Triple-Asset Hub) ---")
    
    # 2. Vision Scan (Fetch Market Data via Redundant Hub)
    prices = await market_hub.get_market_data()
    gold_price = prices.get("XAU/USD")
    
    print(f"[{datetime.now()}] --- PHASE 3: NEWS RADAR (Real-time Audit) ---")
    
    # 3. News Radar (Check fundamental context)
    news_radar_brief = await news_radar.fetch_latest_brief()
    institutional_brief = sovereign_state.get("docs", {}).get("brief", "No institutional brief found.")
    
    combined_news = f"INSTITUTIONAL: {institutional_brief}\nLIVE_RADAR: {news_radar_brief}"
    
    # 4. Sovereign AI Brain Decision (Arabic Stealth Mode)
    print(f"[{datetime.now()}] --- PHASE 4: SOVEREIGN RESULT (Triple-Asset Synthesis) ---")
    
    analysis_context = {
        "prices": prices, # Includes XAU, XAG, DXY, USD/JPY
        "docs": sovereign_state.get("docs", {}),
        "ledger": sovereign_state.get("last_ledger_entry", {}),
        "phase": sovereign_state.get("phase", "UNKNOWN"),
        "session": current_session,
        "session_rules": session_rules,
        "vision_status": "Screenshots failed - using API Data Matrix for Vision Audit"
    }
    
    ai_decision = await brain.analyze_market(analysis_context, combined_news)
    
    # 5. Final Output (Style-Matched Position Defense Report)
    if gold_price:
        sent = await telegram.send_alert(ai_decision.get('reasoning', 'N/A'))
        print(f"[{datetime.now()}] Sequential Intelligence Result Sent: {sent}")
    else:
        print(f"[{datetime.now()}] Sequence Interrupted: Critical Market Data Failure.")
    
    print(f"[{datetime.now()}] --- ANALYSIS SEQUENCE COMPLETE ---")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
