from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import Optional, List, Dict, Any
import logging

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Qdrant client instance
qdrant_client: Optional[QdrantClient] = None


async def init_qdrant() -> None:
    """Initialize Qdrant connection."""
    global qdrant_client
    try:
        qdrant_client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key if settings.qdrant_api_key else None,
        )
        
        # Test connection by getting collections
        collections = qdrant_client.get_collections()
        logger.info(f"Qdrant connection established successfully. Found {len(collections.collections)} collections")
        
    except Exception as e:
        logger.warning(f"Qdrant connection failed (services may not be available yet): {e}")
        # Don't raise - allow app to start without Qdrant for local development


async def close_qdrant() -> None:
    """Close Qdrant connection."""
    global qdrant_client
    try:
        if qdrant_client:
            qdrant_client.close()
            qdrant_client = None
            logger.info("Qdrant connection closed successfully")
    except Exception as e:
        logger.error(f"Error closing Qdrant connection: {e}")


async def get_qdrant() -> QdrantClient:
    """Dependency for getting Qdrant client."""
    if qdrant_client is None:
        raise RuntimeError("Qdrant client not initialized")
    return qdrant_client


async def check_qdrant_health() -> dict:
    """Check Qdrant connectivity and return health status."""
    try:
        if qdrant_client is None:
            return {
                "status": "unhealthy",
                "message": "Qdrant client not initialized"
            }
        
        # Test connection by getting collections
        collections = qdrant_client.get_collections()
        
        return {
            "status": "healthy",
            "message": "Qdrant connection successful",
            "collections_count": len(collections.collections)
        }
    except Exception as e:
        logger.error(f"Qdrant health check failed: {e}")
        return {
            "status": "unhealthy",
            "message": f"Qdrant connection failed: {str(e)}"
        }


async def ensure_collection_exists(
    collection_name: str,
    vector_size: int = 1536,
    distance: Distance = Distance.COSINE
) -> None:
    """Ensure a collection exists, create it if it doesn't."""
    if qdrant_client is None:
        raise RuntimeError("Qdrant client not initialized")
    
    try:
        collections = qdrant_client.get_collections()
        existing_collections = [c.name for c in collections.collections]
        
        if collection_name not in existing_collections:
            qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=distance),
            )
            logger.info(f"Created Qdrant collection: {collection_name}")
        else:
            logger.info(f"Qdrant collection already exists: {collection_name}")
            
    except Exception as e:
        logger.error(f"Failed to ensure collection exists: {e}")
        raise
