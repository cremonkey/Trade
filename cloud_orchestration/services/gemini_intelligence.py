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
        self.institutional_knowledge = self._load_institutional_context()
        self.skills_base = self._load_institutional_skills()
        
        if not api_key:
            self.model = None
            return
            
        genai.configure(api_key=api_key)
        # Using a default but we'll try multiple in analyze_market
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def _load_institutional_context(self) -> str:
        """
        Loads key institutional documents from the knowledge/ directory.
        """
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        knowledge_dir = os.path.join(base_path, "knowledge")
        
        context = ""
        core_files = [
            "goldedge-v5.0-protocol.md",
            "INSTITUTIONAL_WORK_PROTOCOL_v5.0.md",
            "unified_operational_framework_v5.0.md",
            "antigravity-institutional-roadmap.md"
        ]
        
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
        if not os.path.exists(skills_dir):
            return "No skills found."
            
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
        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M")
        
        if not self.model:
            return {"bias": "NEUTRAL", "ftcs_score": 0, "reasoning": "AI Brain Offline", "execute": False}

        prompt = f"""
        (SYSTEM INSTRUCTION):
        {self.SYSTEM_PROMPT}
        
        (INSTITUTIONAL SKILLS & KNOWLEDGE):
        {self.skills_base}
        {self.institutional_knowledge}
        
        (DIRECTIVE):
        Match the exact visual style of the 'Position Defense Report' and 'Master Intelligence Brief'.
        
        (STRUCTURE - ARABIC):
        1. العنوان: (Position Defense Report) - [{time_str}]: 🏛️ 🛡️ ⚖️ 🚀
        2. مقدمة مؤسسية واثقة.
        3. التحليل اللحظي (Tactical Board) مع إشارة للسعر المباشر: ${analysis_context.get('prices', {}).get('XAU/USD')}
        4. قسم الأخبار الفاصلة 🗞️ 🔥 (بناءً على المهارات المفعلة).
        5. التوجيه المؤسسي: (HOLD | BUY | SELL) مع أيقونة 💎.
        6. المعايير الرقمية: (Entry, SL, TP).
        7. الالتزام الاستراتيجي ($5k & $1M Goals).
        8. تذييل بالرموز المتكررة.
        
        (LIVE DATA):
        { {k: v[:2000] for k, v in analysis_context.get('docs', {}).items()} }
        
        Providing decision in JSON:
        {{
          "bias": "BULLISH | BEARISH | NEUTRAL",
          "ftcs_score": 0-100,
          "reasoning": "التقرير الكامل باللغة العربية",
          "execute": true/false
        }}
        """

        # Robust Fallback Strategy (Updated per User Feedback on Gemini 2.5/3.0)
        candidates = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash", "gemini-1.5-flash-latest"]
        last_err = ""
        
        for model_name in candidates:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    prompt,
                    safety_settings={
                        'HATE': 'BLOCK_NONE',
                        'HARASSMENT': 'BLOCK_NONE',
                        'SEXUAL': 'BLOCK_NONE',
                        'DANGEROUS': 'BLOCK_NONE'
                    }
                )
                text = response.text
                return {
                    "bias": "BULLISH" if "BULLISH" in text.upper() else "BEARISH" if "BEARISH" in text.upper() else "NEUTRAL",
                    "ftcs_score": 95,
                    "reasoning": text,
                    "execute": "HOLD" not in text.upper()
                }
            except Exception as e:
                last_error = str(e)
                continue

        error_msg = f"⚠️ **خطأ في عقل النظام بعد عدة محاولات**: {last_error}\n📦 النماذج المجربة: {candidates}"
        return {"reasoning": error_msg, "execute": False}
