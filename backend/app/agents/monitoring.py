from app.core.redis_client import redis_client
import time

class SessionMonitoringAgent:
    def __init__(self):
        self.redis = redis_client

    async def register_session(self, user_id, session_id, meta):
        """
        Registers a new session in Redis using a Hash.
        Meta includes: ip, device, app_name, etc.
        """
        key = self.redis.session_key(user_id, session_id)
        
        # Base session data
        session_data = {
            "user_id": user_id,
            "session_id": session_id,
            "start_time": str(int(time.time())),
            "last_heartbeat": str(int(time.time())),
            "risk_score": "0",  # Initialize as string for Redis
            "status": "ACTIVE",
            **meta # unpacking ip, device, app_name
        }
        
        await self.redis.hset(key, session_data)
        print(f"🕵️ [Monitor] Registered Session: {user_id} :: {session_id} ({meta.get('app_name')})")

    async def heartbeat(self, user_id, session_id):
        """
        Updates the last_heartbeat timestamp and refreshes TTL.
        """
        key = self.redis.session_key(user_id, session_id)
        if await self.redis.get_client().exists(key):
            await self.redis.hset(key, {"last_heartbeat": str(int(time.time()))})
            # print(f"💓 [Monitor] Heartbeat received for {session_id}")
            return True
        return False

    async def get_active_sessions(self, user_id):
        """
        Returns a list of active session dicts for the user.
        """
        pattern = self.redis.session_key(user_id, "*")
        keys = await self.redis.keys(pattern)
        sessions = []
        for key in keys:
            data = await self.redis.hgetall(key)
            if data:
                sessions.append(data)
        return sessions

    async def get_session_data(self, user_id, session_id):
        key = self.redis.session_key(user_id, session_id)
        return await self.redis.hgetall(key)

# Singleton
session_monitor = SessionMonitoringAgent()
