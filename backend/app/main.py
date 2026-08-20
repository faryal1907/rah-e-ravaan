from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import get_settings
from app.core.database import init_db, close_db, check_db_health
from app.core.redis import init_redis, close_redis, check_redis_health
from app.core.qdrant import init_qdrant, close_qdrant, check_qdrant_health
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle events."""
    # Startup
    logger.info("Starting up application...")
    await init_db()
    await init_redis()
    await init_qdrant()
    logger.info("Application startup complete (services may be degraded)")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    try:
        await close_qdrant()
        await close_redis()
        await close_db()
        logger.info("All services closed successfully")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


app = FastAPI(
    title="Rah-e-Ravaan API",
    debug=settings.debug,
    lifespan=lifespan
)


@app.get("/")
def root():
    return {
        "message": "Rah-e-Ravaan backend is running rn",
        "environment": "development" if settings.debug else "production"
    }


@app.get("/health")
async def health():
    """Health check endpoint with service status."""
    db_health = await check_db_health()
    redis_health = await check_redis_health()
    qdrant_health = await check_qdrant_health()
    
    overall_healthy = all([
        db_health["status"] == "healthy",
        redis_health["status"] == "healthy",
        qdrant_health["status"] == "healthy"
    ])
    
    return {
        "status": "healthy" if overall_healthy else "degraded",
        "services": {
            "database": db_health,
            "redis": redis_health,
            "qdrant": qdrant_health
        },
        "environment": "development" if settings.debug else "production"
    }


@app.get("/config")
def config():
    """Return configuration (for debugging - remove in production)"""
    if not settings.debug:
        return {"error": "Configuration endpoint only available in debug mode"}
    
    return {
        "debug": settings.debug,
        "log_level": settings.log_level,
        "cors_origins": settings.cors_origins_list,
        "has_openai_key": bool(settings.openai_api_key),
        "has_anthropic_key": bool(settings.anthropic_api_key),
        "has_qdrant_key": bool(settings.qdrant_api_key)
    }