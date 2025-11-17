from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
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
    settings: Mapped["ProjectSettings"] = relationship(
        "ProjectSettings",
        back_populates="project",
        cascade="all, delete-orphan",
        uselist=False,
    )


class ProjectSettings(Base):
    __tablename__ = "project_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"))

    # Electrical Settings
    system_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Compliance Settings
    require_rohs: Mapped[bool] = mapped_column(Boolean, default=False)
    require_ul: Mapped[bool] = mapped_column(Boolean, default=False)

    project: Mapped["Project"] = relationship("Project", back_populates="settings")
