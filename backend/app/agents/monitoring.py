from app.core.redis_client import redis_client
import time

class SessionMonitoringAgent:
    def __init__(self):
        self.redis = redis_client

    def register_session(self, user_id, session_id, meta):
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
        
        self.redis.hset(key, session_data)
        print(f"🕵️ [Monitor] Registered Session: {user_id} :: {session_id} ({meta.get('app_name')})")

    def heartbeat(self, user_id, session_id):
        """
        Updates the last_heartbeat timestamp and refreshes TTL.
        """
        key = self.redis.session_key(user_id, session_id)
        if self.redis.get_client().exists(key):
            self.redis.hset(key, {"last_heartbeat": str(int(time.time()))})
            # print(f"💓 [Monitor] Heartbeat received for {session_id}")
            return True
        return False

    def get_active_sessions(self, user_id):
        """
        Returns a list of active session dicts for the user.
        """
        pattern = self.redis.session_key(user_id, "*")
        keys = self.redis.keys(pattern)
        sessions = []
        for key in keys:
            data = self.redis.hgetall(key)
            if data:
                sessions.append(data)
        return sessions

    def get_session_data(self, user_id, session_id):
        key = self.redis.session_key(user_id, session_id)
        return self.redis.hgetall(key)

# Singleton
session_monitor = SessionMonitoringAgent()
