import redis.asyncio as redis
from typing import Optional
import logging

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Redis client instance
redis_client: Optional[redis.Redis] = None


async def init_redis() -> None:
    """Initialize Redis connection."""
    global redis_client
    try:
        redis_client = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            max_connections=10,
        )
        
        # Test connection
        await redis_client.ping()
        logger.info("Redis connection established successfully")
        
    except Exception as e:
        logger.warning(f"Redis connection failed (services may not be available yet): {e}")
        # Don't raise - allow app to start without Redis for local development


async def close_redis() -> None:
    """Close Redis connection."""
    global redis_client
    try:
        if redis_client:
            await redis_client.close()
            redis_client = None
            logger.info("Redis connection closed successfully")
    except Exception as e:
        logger.error(f"Error closing Redis connection: {e}")


async def get_redis() -> redis.Redis:
    """Dependency for getting Redis client."""
    if redis_client is None:
        raise RuntimeError("Redis client not initialized")
    return redis_client


async def check_redis_health() -> dict:
    """Check Redis connectivity and return health status."""
    try:
        if redis_client is None:
            return {
                "status": "unhealthy",
                "message": "Redis client not initialized"
            }
        
        await redis_client.ping()
        
        return {
            "status": "healthy",
            "message": "Redis connection successful"
        }
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        return {
            "status": "unhealthy",
            "message": f"Redis connection failed: {str(e)}"
        }
