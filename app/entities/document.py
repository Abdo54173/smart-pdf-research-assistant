from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, String, text
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
    )