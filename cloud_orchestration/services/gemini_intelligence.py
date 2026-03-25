import os
import google.generativeai as genai
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class GeminiIntelligence:
    """
    Antigravity v5.0 AI Intelligence (The Brain).
    Uses Gemini to synthesize market data and news into trading logic.
    """
    
    SYSTEM_PROMPT = """
    You are the 'Sovereign Brain' of the Antigravity v5.0 Trading Suite. 
    Your mission is to analyze market data for XAU/USD (Gold) with institutional precision.

    RULES:
    1. 100% adherence to the Institutional Unit Model (0.01 lot per $100 equity).
    2. Zero trade authorization during Red Folder news (±15 mins).
    3. Mandatory FTCS (Fundamental-Technical Convergence Score) calculation (0-100).
    4. Provide directional bias: BULLISH, BEARISH, or NEUTRAL.
    5. Evaluate SMT Divergence between Gold, Silver (XAG), and DXY.

    OUTPUT FORMAT (JSON):
    {
      "bias": "STRING",
      "ftcs_score": INTEGER,
      "reasoning": "STRING",
      "execute": BOOLEAN
    }
    """

    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if not api_key:
            # Fallback or error handling
            self.model = None
            return
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=self.SYSTEM_PROMPT
        )

    async def analyze_market(self, market_data: Dict[str, Any], news_data: str) -> Dict[str, Any]:
        """
        Synthesizes technical and fundamental data into a Sovereign Decision.
        """
        if not self.model:
            return {"bias": "NEUTRAL", "ftcs_score": 0, "reasoning": "AI Brain Offline", "execute": False}

        prompt = f"""
        DATA INPUT:
        Market Prices: {market_data}
        Recent News/Fundamentals: {news_data}
        
        Analyze the data and provide a Sovereign Decision.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Simple simulation of JSON extraction (ideal to use response_mime_type in actual implementation)
            # For now, we return a structured response
            return {
                "bias": "BULLISH", # Mock result for now
                "ftcs_score": 85,
                "reasoning": response.text[:200],
                "execute": True
            }
        except Exception as e:
            return {"error": str(e), "execute": False}
