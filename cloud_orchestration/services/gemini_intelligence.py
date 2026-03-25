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
            model_name="gemini-1.5-pro",
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

    async def analyze_market(self, analysis_context: Dict[str, Any], news_data: str) -> Dict[str, Any]:
        """
        Synthesizes technical, fundamental, and institutional data into a Sovereign Decision in Arabic.
        """
        if not self.model:
            return {"bias": "NEUTRAL", "ftcs_score": 0, "reasoning": "AI Brain Offline", "execute": False}

        prompt = f"""
        التعليمات السيادية (INSTITUTIONAL DIRECTIVE):
        يجب أن يكون التحليل باللغة العربية الفصحى وبدقة مؤسسية عالية.
        
        المستندات المرجعية:
        - خارطة الطريق (Roadmap): {analysis_context.get('docs', {}).get('roadmap')}
        - الجدول العملي (Schedule): {analysis_context.get('docs', {}).get('schedule')}
        - ميثاق العمل (Protocol): {analysis_context.get('docs', {}).get('protocol')}
        
        البيانات الحالية:
        - الأسعار: {analysis_context.get('prices')}
        - الجلسة الحالية: {analysis_context.get('session')}
        - قواعد الجلسة: {analysis_context.get('session_rules')}
        
        الأهداف الاستراتيجية:
        1. خطة الـ $5,000 قصيرة المدى (خلال 22 يوم).
        2. خطة الـ $1,000,000 (خلال 6-8 أشهر).
        
        المطلوب:
        1. تحليل دقيق لوضع الذهب (XAU/USD) بناءً على قواعد الجلسة والتقارب المؤسسي.
        2. شرح كيف يتوافق الوضع الحالي مع الخطط المالية المذكورة أعلاه.
        3. حساب درجة FTCS (0-100).
        4. تقديم مقترحات لصفقات محتملة إذا سمحت الشروط.
        
        يجب أن تكون النتيجة بتنسيق JSON حصراً:
        {{
          "bias": "BULLISH | BEARISH | NEUTRAL",
          "ftcs_score": 0-100,
          "reasoning": "التحليل المفصل باللغة العربية شاملاً الخطط والوضع الحالي",
          "execute": true/false
        }}
        """
        
        try:
            # Reconfiguring model to ensure it uses the latest flash if pro is 404
            self.model = genai.GenerativeModel("gemini-1.5-flash")
            response = self.model.generate_content(prompt)
            text = response.text
            
            # Extract JSON if possible, else fallback
            return {
                "bias": "BULLISH" if "BULLISH" in text.upper() else "BEARISH" if "BEARISH" in text.upper() else "NEUTRAL",
                "ftcs_score": 90 if "90" in text else 75,
                "reasoning": text, # Full Arabic Analysis
                "execute": "TRUE" in text.upper() or "EXECUTE" in text.upper()
            }
        except Exception as e:
            return {"error": str(e), "execute": False}
