import redis.asyncio as redis
from app.core.config import settings
import os

# Create Async Redis Client
# Force 127.0.0.1 to avoid Windows IPv6/Localhost issues
REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")

try:
    redis_client = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    print(f"✅ Database (Async) Connected to {REDIS_URL}")
except Exception as e:
    print(f"❌ Database Connection Failed: {e}")
    redis_client = None

async def get_redis():
    if redis_client is None:
        raise Exception("Redis not available")
    return redis_client
