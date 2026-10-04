from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PipePart(Base):
    __tablename__ = "pipe_parts"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    pipe_id: Mapped[int] = mapped_column(
        ForeignKey("pipes.id"),
        nullable=False,
    )

    condition: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    length: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    pipe: Mapped["Pipe"] = relationship(
        "Pipe",
        back_populates="parts",
    )