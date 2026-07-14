from fastapi import APIRouter
from sqlalchemy import text

from app.database.session import AsyncSessionLocal

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health_check():
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception as ex:
        return {
            "status": "unhealthy",
            "database": str(ex),
        }