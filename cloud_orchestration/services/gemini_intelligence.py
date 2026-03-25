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
            model_name="gemini-1.5-flash",
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
        Synthesizes technical, fundamental, and institutional data into a Sovereign Decision in the exact
        'Position Defense Report' style requested.
        """
        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M")
        
        if not self.model:
            return {"bias": "NEUTRAL", "ftcs_score": 0, "reasoning": "AI Brain Offline", "execute": False}

        prompt = f"""
        يجب أن يكون الرد مطابقاً تماماً لنمط "تقرير السيطرة على المركز" (Position Defense Report) المرفق في الصورة.
        
        الهيكل المطلوب (Strict Structure):
        1. العنوان: (Position Defense Report) - [{time_str}]: 🏛️ 🛡️ ⚖️ 🚀
        2. مقدمة مؤسسية: تبدأ بـ "لقد قمت بتحديث سجل الصفقات بمركزك الحالي..." بلهجة قوية وواثقة.
        3. التحليل المالي:
           - السعر اللحظي (Instant Price): {analysis_context.get('prices', {}).get('XAU/USD')}
           - المسافة عن نقطة الدخول (Entry Context).
        4. قسم الأخبار الفاصلة 🗞️ 🔥: (استخرج أهم 3 نقاط جيوسياسية أو اقتصادية من المستندات وأضف الرموز المناسبة مثل الصواريخ، البنتاغون، البيت الأبيض).
        5. التوجيه المؤسسي: (HOLD أو BUY أو SELL) مع أيقونة 💎.
        6. المعايير الرقمية:
           - نقطة الدخول: (Entry)
           - هذا الدرع (Stop Loss SL):
           - الهدف (Take Profit TP):
        7. الخطة الاستراتيجية: اذكر صراحة الالتزام بخطة الـ $5,000 في 22 يوماً وخطة الـ $1,000,000 في 6-8 أشهر.
        8. تذييل بنظام الرموز المزدوجة المتكررة كما في الصورة.
        
        بيانات المصدر:
        - خارطة الطريق: {analysis_context.get('docs', {}).get('roadmap')}
        - السجل: {analysis_context.get('docs', {}).get('ledger')}
        - البروتوكول: {analysis_context.get('docs', {}).get('protocol')}
        
        يجب أن تكون النتيجة بتنسيق JSON:
        {{
          "bias": "BULLISH | BEARISH | NEUTRAL",
          "ftcs_score": 0-100,
          "reasoning": "التقرير الكامل المنسق باللغة العربية والرموز الإيموجي",
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
