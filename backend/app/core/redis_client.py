import redis
import os
import json

class RedisClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            # Force 127.0.0.1 to avoid Windows localhost/IPv6 issues
            cls._instance.client = redis.from_url(os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"), decode_responses=True)
            cls._instance.SESSION_TTL = 300  # 5 Minutes
        return cls._instance

    def get_client(self):
        return self.client

    def session_key(self, user_id, session_id):
        return f"session:{user_id}:{session_id}"

    # Hash Operations
    def hset(self, key, mapping):
        """Set multiple fields in a hash."""
        self.client.hset(key, mapping=mapping)
        self.client.expire(key, self.SESSION_TTL)

    def hgetall(self, key):
        """Get all fields from a hash."""
        return self.client.hgetall(key)
    
    def hincrby(self, key, field, amount=1):
        """Increment a specific field (e.g. risk_score) in the hash."""
        val = self.client.hincrby(key, field, amount)
        self.client.expire(key, self.SESSION_TTL) # Refresh TTL on activity
        return val
        
    def hget(self, key, field):
        """Get a single field."""
        return self.client.hget(key, field)

    def expire(self, key, ttl=None):
        if ttl is None:
            ttl = self.SESSION_TTL
        self.client.expire(key, ttl)

    def delete(self, key):
        self.client.delete(key)
    
    def keys(self, pattern):
        return self.client.keys(pattern)

# Singleton accessor
redis_client = RedisClient()
