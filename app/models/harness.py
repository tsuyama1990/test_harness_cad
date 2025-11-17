from __future__ import annotations

import uuid
from typing import List

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Harness(Base):
    __tablename__ = "harnesses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str | None] = mapped_column(String, index=True, nullable=True)

    connectors: Mapped[List["Connector"]] = relationship(
        "Connector", back_populates="harness", cascade="all, delete-orphan"
    )
    wires: Mapped[List["Wire"]] = relationship(
        "Wire", back_populates="harness", cascade="all, delete-orphan"
    )
    connections: Mapped[List["Connection"]] = relationship(
        "Connection", back_populates="harness", cascade="all, delete-orphan"
    )


class Connector(Base):
    __tablename__ = "connectors"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    logical_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    manufacturer: Mapped[str] = mapped_column(String, nullable=False)
    part_number: Mapped[str] = mapped_column(String, nullable=False)
    harness_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("harnesses.id"), nullable=False
    )

    harness: Mapped[Harness] = relationship("Harness", back_populates="connectors")
    pins: Mapped[List["Pin"]] = relationship(
        "Pin", back_populates="connector", cascade="all, delete-orphan"
    )


class Pin(Base):
    __tablename__ = "pins"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    logical_id: Mapped[str] = mapped_column(String, nullable=False)
    connector_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("connectors.id"), nullable=False
    )

    connector: Mapped[Connector] = relationship("Connector", back_populates="pins")


class Wire(Base):
    __tablename__ = "wires"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    logical_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    manufacturer: Mapped[str] = mapped_column(String, nullable=False)
    part_number: Mapped[str] = mapped_column(String, nullable=False)
    color: Mapped[str] = mapped_column(String, nullable=False)
    gauge: Mapped[float] = mapped_column(Float, nullable=False)
    length: Mapped[float] = mapped_column(Float, nullable=False)
    harness_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("harnesses.id"), nullable=False
    )

    harness: Mapped[Harness] = relationship("Harness", back_populates="wires")


class Connection(Base):
    __tablename__ = "connections"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    harness_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("harnesses.id"), nullable=False
    )
    wire_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("wires.id"), nullable=False
    )
    from_pin_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("pins.id"), nullable=False
    )
    to_pin_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("pins.id"), nullable=False
    )

    # Assembly instructions
    strip_length_a: Mapped[float | None] = mapped_column(Float, nullable=True)
    strip_length_b: Mapped[float | None] = mapped_column(Float, nullable=True)
    terminal_part_number_a: Mapped[str | None] = mapped_column(String, nullable=True)
    terminal_part_number_b: Mapped[str | None] = mapped_column(String, nullable=True)
    marking_text_a: Mapped[str | None] = mapped_column(String, nullable=True)
    marking_text_b: Mapped[str | None] = mapped_column(String, nullable=True)

    harness: Mapped[Harness] = relationship("Harness", back_populates="connections")
    wire: Mapped[Wire] = relationship("Wire")
    from_pin: Mapped[Pin] = relationship("Pin", foreign_keys=[from_pin_id])
    to_pin: Mapped[Pin] = relationship("Pin", foreign_keys=[to_pin_id])
