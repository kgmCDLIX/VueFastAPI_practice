from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Vertex(Base):
    __tablename__ = "vertices"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    condition: Mapped[str | None] = mapped_column(String(100), nullable=True)

    pipes_started: Mapped[list["Pipe"]] = relationship(
        "Pipe",
        foreign_keys="Pipe.vertex_start_id",
        back_populates="vertex_start",
    )

    pipes_ended: Mapped[list["Pipe"]] = relationship(
        "Pipe",
        foreign_keys="Pipe.vertex_end_id",
        back_populates="vertex_end",
    )