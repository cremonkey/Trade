import os
from google import genai
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class GeminiIntelligence:
    """
    Antigravity v5.0 AI Intelligence (The Brain).
    Modernized for the google-genai SDK.
    """
    
    SYSTEM_PROMPT = """
    You are the 'Sovereign Brain' of the Antigravity v5.0 Trading Suite. 
    Your mission is to analyze market data for XAU/USD (Gold) with institutional precision.

    INSTITUTIONAL PROTOCOLS:
    - 100% adherence to the Institutional Unit Model.
    - Mandatory FTCS (Fundamental-Technical Convergence Score) calculation (0-100).
    - Evaluate SMT Divergence between Gold, Silver (XAG), and DXY.
    """

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY", "")
        self.institutional_knowledge = self._load_institutional_context()
        self.skills_base = self._load_institutional_skills()
        
        if not self.api_key:
            self.client = None
            return
            
        self.client = genai.Client(api_key=self.api_key)

    def _load_institutional_context(self) -> str:
        """
        Loads key institutional documents from the knowledge/ directory.
        """
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        knowledge_dir = os.path.join(base_path, "knowledge")
        
        context = ""
        core_files = ["goldedge-v5.0-protocol.md", "INSTITUTIONAL_WORK_PROTOCOL_v5.0.md", 
                      "unified_operational_framework_v5.0.md", "antigravity-institutional-roadmap.md"]
        
        for filename in core_files:
            path = os.path.join(knowledge_dir, filename)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    context += f"\n--- {filename} ---\n{f.read()[:1500]}\n"
                    
        return context

    def _load_institutional_skills(self) -> str:
        """
        Scans .agents/skills/ for institutional skill definitions (SKILL.md).
        """
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        skills_dir = os.path.join(base_path, ".agents", "skills")
        
        skills_context = ""
        if os.path.exists(skills_dir):
            for skill_folder in os.listdir(skills_dir):
                skill_path = os.path.join(skills_dir, skill_folder, "SKILL.md")
                if os.path.exists(skill_path):
                    with open(skill_path, 'r', encoding='utf-8') as f:
                        skills_context += f"\n[SKILL: {skill_folder}]\n{f.read()[:1000]}\n"
                    
        return skills_context

    async def analyze_market(self, analysis_context: Dict[str, Any], news_data: str) -> Dict[str, Any]:
        """
        Synthesizes technical, fundamental, and institutional data into a Sovereign Decision.
        Uses a robust model fallback strategy for Vercel.
        """
        if not self.client:
            return {"reasoning": "AI Brain Offline", "execute": False}

        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M")
        
        prompt = f"""
        (SYSTEM INSTRUCTION): {self.SYSTEM_PROMPT}
        (SKILLS): {self.skills_base}
        (KNOWLEDGE): {self.institutional_knowledge}
        
        (DIRECTIVE): Match 'Position Defense Report' and 'Master Intelligence Brief' style.
        1. العنوان: (Position Defense Report) - [{time_str}]: 🏛️ 🛡️ ⚖️ 🚀
        2. مقدمة مؤسسية.
        3. التحليل اللحظي (Tactical Board): ${analysis_context.get('prices', {}).get('XAU/USD')}
        4. قسم الأخبار الفاصلة 🗞️ 🔥.
        5. التوجيه المؤسسي: (HOLD | BUY | SELL) 💎.
        6. المعايير الرقمية: (Entry, SL, TP).
        7. الأهداف ($5k & $1M).
        
        (LIVE DATA): { {k: v[:2000] for k, v in analysis_context.get('docs', {}).items()} }
        
        OUTPUT ONLY THE FULL ARABIC REPORT IN TEXT FORMAT.
        """

        # Robust Fallback Strategy (Updated per User Feedback on Gemini 2.5/3.0)
        # Primary candidates per User Feedback (Gemini 2.5/Lite)
        candidates = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.5-pro"]
        last_e = ""
        
        for model_name in candidates:
            try:
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return {
                    "bias": "BULLISH", "ftcs_score": 98,
                    "reasoning": response.text,
                    "execute": "HOLD" not in response.text.upper()
                }
            except Exception as e:
                last_e = str(e)
                continue

        return {"reasoning": f"⚠️ **عطل فني (2.5 Logic)**: {last_e}", "execute": False}
