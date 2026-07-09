from fastapi import APIRouter
from sqlalchemy import text

from app.database.session import SessionLocal

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def health_check():
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception as ex:
        return {
            "status": "unhealthy",
            "database": str(ex),
        }