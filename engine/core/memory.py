import os
import time
from typing import List, Dict
from utils.supabase_client import supabase_client

class AegisMemory:
    """
    Persistence layer for short-term conversation and long-term user context.
    Uses Supabase (Postgres) for global, stateless persistence.
    """
    def __init__(self):
        self.client = supabase_client

    def add_message(self, session_id: str, role: str, content: str):
        """Persists a new message to the conversation table in Supabase."""
        try:
            self.client.table("conversations").insert({
                "session_id": session_id,
                "role": role,
                "content": content,
                "timestamp": time.time()
            }).execute()
        except Exception as e:
            print(f"Memory Persistence Error: {e}")

    def get_history(self, session_id: str, k: int = 10) -> List[Dict]:
        """Retrieves the last K messages for a given session."""
        try:
            res = self.client.table("conversations") \
                .select("role, content") \
                .eq("session_id", session_id) \
                .order("timestamp", desc=True) \
                .limit(k) \
                .execute()
            
            # Reverse to maintain chronological order for the LLM context
            return [{"role": r['role'], "content": r['content']} for r in reversed(res.data)]
        except Exception as e:
            print(f"Memory Retrieval Error: {e}")
            return []

    def save_fact(self, user_id: str, fact: str):
        """Saves a long-term fact about the user."""
        try:
            self.client.table("facts").insert({
                "user_id": user_id,
                "fact": fact,
                "timestamp": time.time()
            }).execute()
        except Exception as e:
            print(f"Fact Persistence Error: {e}")

memory = AegisMemory()
