from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ConversationDocument(Base):
    __tablename__ = "conversation_documents"

    conversation_id: Mapped[str] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"),
        primary_key=True,
    )

    document_id: Mapped[str] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        primary_key=True,
    )