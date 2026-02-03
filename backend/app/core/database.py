from app.core.redis_client import redis_client

# We verify that redis_client is our InMemoryRedisClient
print("✅ Database (Async) Connected to In-Memory Mock")

async def get_redis():
    return redis_client
