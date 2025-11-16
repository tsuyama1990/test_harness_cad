from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.harness_design import HarnessDesign


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True, unique=True)

    harness_designs: Mapped[List["HarnessDesign"]] = relationship(
        "HarnessDesign", back_populates="project"
    )
