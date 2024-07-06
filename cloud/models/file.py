from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, func
from sqlalchemy import String, TIMESTAMP

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, TEXT
import uuid
from datetime import datetime
from db import Base


class File(Base):
    __tablename__ = "file"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(TEXT())
    ext: Mapped[str] = mapped_column(TEXT(), nullable=True)
    hash: Mapped[str] = mapped_column(TEXT())
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)

    def __repr__(self) -> str:
        return f"File(id={self.id!r}, name={self.name!r}, ext={self.ext!r}, hash={self.hash!r}, created_at={self.created_at!r}, created_by={self.created_by!r})"
