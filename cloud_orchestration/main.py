import os
import datetime
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

app = FastAPI(title="Antigravity Sovereign Cloud")

# Initialize components
risk_manager = RiskManager()
execution = ExecutionSpecialist()
news_analyst = NewsAnalyst()
brain = GeminiIntelligence()
supabase = SupabaseIntegration()
telegram = TelegramIntegration()
twelve_data = TwelveDataIntegration()

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
    
    # 1. Fetch market data
    prices = await twelve_data.get_market_data()
    gold_price = prices.get("XAU/USD")
    print(f"[{datetime.now()}] Market Data: {prices}")
    
    # 2. Check risk & config
    try:
        config = supabase.get_system_config()
        print(f"[{datetime.now()}] System Config: {config}")
    except Exception as e:
        print(f"[{datetime.now()}] Supabase Error: {e}")
        return

    equity = config.get("equity", 88.00)
    lot_size = risk_manager.calculate_lot_size(equity)
    
    # 3. AI Brain Analysis
    news_summary = "XAU/USD seeking liquidity. Institutional bias evaluation requested."
    ai_decision = await brain.analyze_market(prices, news_summary)
    print(f"[{datetime.now()}] Brain Decision: {ai_decision}")
    
    ftcs = ai_decision.get("ftcs_score", 0)
    bias = ai_decision.get("bias", "NEUTRAL")
    
    # 4. Push Alerts
    if gold_price:
        status_emoji = "✅ EXECUTE" if ai_decision.get("execute") else "⚠️ WATCH"
        sent = await telegram.send_alert(
            f"🧠 **Brain Decision**: {status_emoji}\n"
            f"--- \n"
            f"💰 XAU/USD: ${gold_price}\n"
            f"📊 FTCS: {ftcs}\n"
            f"🎯 Bias: {bias}\n"
            f"🛡️ Reasoning: {ai_decision.get('reasoning', 'N/A')}"
        )
        print(f"[{datetime.now()}] Telegram Alert Sent: {sent}")
    else:
        print(f"[{datetime.now()}] Skipping Telegram Alert: No Gold Price found.")
    
    print(f"[{datetime.now()}] Analysis cycle completed.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
