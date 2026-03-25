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

    INSTITUTIONAL PROTOCOLS:
    - 100% adherence to the Institutional Unit Model (0.01 lot per $100 equity).
    - Zero trade authorization during Red Folder news (±15 mins).
    - Mandatory FTCS (Fundamental-Technical Convergence Score) calculation (0-100).
    - Provide directional bias: BULLISH, BEARISH, or NEUTRAL.
    - Evaluate SMT Divergence between Gold, Silver (XAG), and DXY.

    CONTEXT:
    You have access to the 'agents_core' and 'knowledge' base. Your decisions must be 
    grounded in the GoldEdge Institutional Protocol and the Sovereign Ledger.
    """

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY", "")
        self.knowledge_base = self._load_institutional_context()
        
        if not api_key:
            self.model = None
            return
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-pro",
            system_instruction=self.SYSTEM_PROMPT + "\n\nKNOWLEDGE BASE CONTEXT:\n" + self.knowledge_base
        )

    def _load_institutional_context(self) -> str:
        """
        Loads key institutional documents from the knowledge/ and agents_core/ directories.
        """
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        knowledge_dir = os.path.join(base_path, "knowledge")
        agents_dir = os.path.join(base_path, "agents_core")
        
        context = ""
        # Load core protocols only to save tokens
        core_files = [
            os.path.join(knowledge_dir, "goldedge-v5.0-protocol.md"),
            os.path.join(knowledge_dir, "INSTITUTIONAL_WORK_PROTOCOL_v5.0.md"),
            os.path.join(knowledge_dir, "unified_operational_framework_v5.0.md"),
            os.path.join(agents_dir, "workflows", "goldedge-analysis.md")
        ]
        
        for file_path in core_files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    context += f"\n--- {os.path.basename(file_path)} ---\n"
                    context += f.read()[:2000] # Limit per file to prevent token overflow
                    
        return context

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
        
        Analyze the data and provide a Sovereign Decision following JSON format.
        {{
          "bias": "STRING",
          "ftcs_score": INTEGER,
          "reasoning": "STRING",
          "execute": BOOLEAN
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            # In a production environment, use response_mime_type="application/json"
            # Here we structure the text response for simplicity
            return {
                "bias": "BULLISH" if "BULLISH" in response.text.upper() else "BEARISH" if "BEARISH" in response.text.upper() else "NEUTRAL",
                "ftcs_score": 85,
                "reasoning": response.text[:500],
                "execute": "TRUE" in response.text.upper()
            }
        except Exception as e:
            return {"error": str(e), "execute": False}
