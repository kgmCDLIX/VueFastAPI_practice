from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Pipe(Base):
    __tablename__ = "pipes"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    vertex_start_id: Mapped[int] = mapped_column(
        ForeignKey("vertices.id"),
        nullable=False,
    )

    vertex_end_id: Mapped[int] = mapped_column(
        ForeignKey("vertices.id"),
        nullable=False,
    )

    condition: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    diameter: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    material: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    vertex_start: Mapped["Vertex"] = relationship(
        "Vertex",
        foreign_keys=[vertex_start_id],
        back_populates="pipes_started",
    )

    vertex_end: Mapped["Vertex"] = relationship(
        "Vertex",
        foreign_keys=[vertex_end_id],
        back_populates="pipes_ended",
    )

    parts: Mapped[list["PipePart"]] = relationship(
        "PipePart",
        back_populates="pipe",
        cascade="all, delete-orphan",
    )