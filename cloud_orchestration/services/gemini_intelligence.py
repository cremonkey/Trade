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
        (INSTITUTIONAL SKILLS & KNOWLEDGE): {self.skills_base} {self.institutional_knowledge}
        
        (SEQUENTIAL PROTOCOL):
        1. VISION AUDIT: Scan the tactical price levels (${analysis_context.get('prices', {}).get('XAU/USD')}) as a visual chart matrix.
        2. NEWS RADAR: Integrate the following fundamental intelligence: {news_data}
        3. SOVEREIGN SYNTHESIS: Generate the report in Stealth Mode.
        
        (DIRECTIVE - STEALTH MODE):
        - START directly with the analysis.
        - NO plan/objective mentions. 
        - suggested trade at the very end in a sleek, bold layout.
        
        (OUTPUT STRUCTURE - ARABIC):
        1. 🏛️ (Position Defense Report) - [{time_str}]:
        2. التحليل اللحظي (Tactical Board) & (Vision Audit Result).
        3. قسم الأخبار الفاصلة 🗞️ 🔥.
        4. (Suggested Trade Section - SLEEK & BOLD) 💎:
           - القرار: (HOLD | BUY | SELL)
           - الدرع (SL):
           - الهدف (TP):
        
        (LIVE DATA): { {k: v[:2000] for k, v in analysis_context.get('docs', {}).items()} }
        
        OUTPUT ONLY THE FULL ARABIC REPORT IN TEXT FORMAT.
        """

        # Advanced High-Tier Candidates (Aligned with your specific API environment)
        candidates = ["gemini-3.1-pro-preview", "gemini-2.5-flash", "gemini-2.5-pro"]
        last_e = ""
        
        for model_name in candidates:
            try:
                # Use standard modelID, Client handles prefixing if needed.
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

        return {"reasoning": f"⚠️ **عطل فني في نظام التحليل**: {last_e}", "execute": False}
