import os
import json
import time
import fnmatch

class InMemoryRedisClient:
    _instance = None
    _store = {} # Key -> Value
    _hash_store = {} # Key -> { field: value }
    _set_store = {} # Key -> Set()
    _ttls = {} # Key -> Expiry Timestamp

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InMemoryRedisClient, cls).__new__(cls)
            cls._instance.SESSION_TTL = 300 
            print("✅ [Core] In-Memory Redis Mock Initialized (Async Mode)")
        return cls._instance

    def get_client(self):
        return self

    def session_key(self, user_id, session_id):
        return f"session:{user_id}:{session_id}"

    async def _check_expiry(self, key):
        if key in self._ttls:
            if time.time() > self._ttls[key]:
                await self.delete(key)
                return True
        return False

    # Hash Operations
    async def hset(self, key, mapping):
        await self._check_expiry(key)
        if key not in self._hash_store:
            self._hash_store[key] = {}
        self._hash_store[key].update(mapping)
        await self.expire(key, self.SESSION_TTL)

    async def hgetall(self, key):
        if await self._check_expiry(key): return {}
        return self._hash_store.get(key, {})
    
    async def hincrby(self, key, field, amount=1):
        await self._check_expiry(key)
        if key not in self._hash_store:
            self._hash_store[key] = {}
        
        current = int(self._hash_store[key].get(field, 0))
        new_val = current + amount
        self._hash_store[key][field] = str(new_val)
        await self.expire(key, self.SESSION_TTL)
        return new_val
        
    async def hget(self, key, field):
        if await self._check_expiry(key): return None
        return self._hash_store.get(key, {}).get(field)

    async def expire(self, key, ttl=None):
        if ttl is None:
            ttl = self.SESSION_TTL
        self._ttls[key] = time.time() + ttl

    async def delete(self, key):
        if key in self._store: del self._store[key]
        if key in self._hash_store: del self._hash_store[key]
        if key in self._set_store: del self._set_store[key]
        if key in self._ttls: del self._ttls[key]
    
    async def keys(self, pattern):
        # Scan all stores
        all_keys = list(self._store.keys()) + list(self._hash_store.keys()) + list(self._set_store.keys())
        # Simple glob matching
        return fnmatch.filter(all_keys, pattern)

    # Simple KV Operations
    async def get(self, key):
        if await self._check_expiry(key): return None
        return self._store.get(key)

    async def set(self, key, value, ex=None):
        self._store[key] = value
        await self.expire(key, ex if ex else self.SESSION_TTL)
    
    async def setex(self, key, time, value):
        # time can be seconds (int) or timedelta
        if hasattr(time, 'total_seconds'):
            time = int(time.total_seconds())
        await self.set(key, value, ex=time)
        
    async def exists(self, key):
        await self._check_expiry(key)
        return (key in self._store or key in self._hash_store or key in self._set_store)

    # Set Operations
    async def sadd(self, key, member):
        await self._check_expiry(key)
        if key not in self._set_store:
            self._set_store[key] = set()
        self._set_store[key].add(member)
        await self.expire(key, self.SESSION_TTL)

    async def smembers(self, key):
        if await self._check_expiry(key): return set()
        return self._set_store.get(key, set())
        
    async def srem(self, key, member):
        await self._check_expiry(key)
        if key in self._set_store:
            self._set_store[key].discard(member)
            if not self._set_store[key]:
                del self._set_store[key]

# Singleton accessor
redis_client = InMemoryRedisClient()
