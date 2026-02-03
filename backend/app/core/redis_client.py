import os
import json
import time
import fnmatch

class InMemoryRedisClient:
    _instance = None
    _store = {} # Key -> Value
    _hash_store = {} # Key -> { field: value }
    _ttls = {} # Key -> Expiry Timestamp

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InMemoryRedisClient, cls).__new__(cls)
            cls._instance.SESSION_TTL = 300 
            print("✅ [Core] In-Memory Redis Mock Initialized")
        return cls._instance

    def get_client(self):
        return self

    def session_key(self, user_id, session_id):
        return f"session:{user_id}:{session_id}"

    def _check_expiry(self, key):
        if key in self._ttls:
            if time.time() > self._ttls[key]:
                self.delete(key)
                return True
        return False

    # Hash Operations
    def hset(self, key, mapping):
        self._check_expiry(key)
        if key not in self._hash_store:
            self._hash_store[key] = {}
        self._hash_store[key].update(mapping)
        self.expire(key, self.SESSION_TTL)

    def hgetall(self, key):
        if self._check_expiry(key): return {}
        return self._hash_store.get(key, {})
    
    def hincrby(self, key, field, amount=1):
        self._check_expiry(key)
        if key not in self._hash_store:
            self._hash_store[key] = {}
        
        current = int(self._hash_store[key].get(field, 0))
        new_val = current + amount
        self._hash_store[key][field] = str(new_val)
        self.expire(key, self.SESSION_TTL)
        return new_val
        
    def hget(self, key, field):
        if self._check_expiry(key): return None
        return self._hash_store.get(key, {}).get(field)

    def expire(self, key, ttl=None):
        if ttl is None:
            ttl = self.SESSION_TTL
        self._ttls[key] = time.time() + ttl

    def delete(self, key):
        if key in self._store: del self._store[key]
        if key in self._hash_store: del self._hash_store[key]
        if key in self._ttls: del self._ttls[key]
    
    def keys(self, pattern):
        # Scan both stores
        all_keys = list(self._store.keys()) + list(self._hash_store.keys())
        # Simple glob matching
        return fnmatch.filter(all_keys, pattern)

    # Simple KV Operations (used by Risk Agent for last_switch_key)
    def get(self, key):
        if self._check_expiry(key): return None
        return self._store.get(key)

    def set(self, key, value):
        self._store[key] = value
        self.expire(key, self.SESSION_TTL)
        
    def exists(self, key):
        self._check_expiry(key)
        return (key in self._store or key in self._hash_store)

# Singleton accessor
redis_client = InMemoryRedisClient()
