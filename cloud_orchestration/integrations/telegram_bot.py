import os
import httpx
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class TelegramIntegration:
    """
    Simple Telegram interface for sending alerts and processing commands.
    """
    
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    async def send_alert(self, message: str, parse_mode: str = "Markdown") -> bool:
        """
        Sends a push notification to the user's phone.
        """
        if not self.token or not self.chat_id:
            return False
            
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": parse_mode
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(self.api_url, json=payload)
            return response.status_code == 200

    def format_status_report(self, data: dict) -> str:
        """
        Formats a consolidated Markdown brief for the /status command.
        """
        report = (
            f"🏛️ **Antigravity Sovereign Status**\n"
            f"--- \n"
            f"💰 **Balance**: ${data.get('balance', '0.00')}\n"
            f"📊 **Equity**: ${data.get('equity', '0.00')}\n"
            f"📉 **Current Lot**: {data.get('lot_size', '0.01')}\n"
            f"📅 **Phase**: {data.get('phase', 'Moonshot')}\n"
            f"--- \n"
            f"🛡️ **System State**: {'🔴 LOCKED' if data.get('is_locked') else '🟢 ACTIVE'}\n"
        )
        return report
