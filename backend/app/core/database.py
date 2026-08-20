from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from typing import Optional
import logging

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Create async engine
engine = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Dependency for getting async database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database connection and create tables."""
    try:
        # Test connection
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection established successfully")
        
        # Create all tables (in production, use Alembic migrations instead)
        # async with engine.begin() as conn:
        #     await conn.run_sync(Base.metadata.create_all)
        
    except Exception as e:
        logger.warning(f"Database connection failed (services may not be available yet): {e}")
        # Don't raise - allow app to start without database for local development


async def close_db() -> None:
    """Close database connections."""
    try:
        await engine.dispose()
        logger.info("Database connections closed successfully")
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")


async def check_db_health() -> dict:
    """Check database connectivity and return health status."""
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            result.fetchone()
        
        return {
            "status": "healthy",
            "message": "Database connection successful"
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}"
        }
