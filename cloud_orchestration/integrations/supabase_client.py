import os
from supabase import create_client, Client
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

class SupabaseIntegration:
    """
    Wrapper for Supabase client to handle trading journal and system config.
    """
    
    def __init__(self):
        url: str = os.getenv("SUPABASE_URL", "")
        key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
        if not url or not key:
            raise ValueError("SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY not set")
        self.supabase: Client = create_client(url, key)

    def get_system_config(self) -> Dict[str, Any]:
        """
        Retrieves the latest system configuration.
        """
        response = self.supabase.table("system_config").select("*").limit(1).execute()
        return response.data[0] if response.data else {}

    def update_balance(self, new_balance: float, new_equity: float):
        """
        Updates the account balance and equity in system_config.
        """
        return self.supabase.table("system_config").update({
            "balance": new_balance,
            "equity": new_equity,
            "updated_at": "now()"
        }).eq("id", 1).execute()

    def add_trade(self, trade_data: Dict[str, Any]):
        """
        Adds a new trade entry to the trading_history table.
        """
        return self.supabase.table("trading_history").insert(trade_data).execute()

    def get_recent_trades(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieves the most recent trades from the journal.
        """
        response = self.supabase.table("trading_history")\
            .select("*")\
            .order("timestamp", desc=True)\
            .limit(limit)\
            .execute()
        return response.data
