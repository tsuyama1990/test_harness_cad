import uuid

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Harness(Base):
    __tablename__ = "harnesses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)

    connectors = relationship(
        "Connector", back_populates="harness", cascade="all, delete-orphan"
    )
    wires = relationship("Wire", back_populates="harness", cascade="all, delete-orphan")
    connections = relationship(
        "Connection", back_populates="harness", cascade="all, delete-orphan"
    )


class Connector(Base):
    __tablename__ = "connectors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    logical_id = Column(String, index=True, nullable=False)
    manufacturer = Column(String, nullable=False)
    part_number = Column(String, nullable=False)
    harness_id = Column(UUID(as_uuid=True), ForeignKey("harnesses.id"), nullable=False)

    harness = relationship("Harness", back_populates="connectors")
    pins = relationship("Pin", back_populates="connector", cascade="all, delete-orphan")


class Pin(Base):
    __tablename__ = "pins"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    logical_id = Column(String, nullable=False)
    connector_id = Column(
        UUID(as_uuid=True), ForeignKey("connectors.id"), nullable=False
    )

    connector = relationship("Connector", back_populates="pins")


class Wire(Base):
    __tablename__ = "wires"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    logical_id = Column(String, index=True, nullable=False)
    manufacturer = Column(String, nullable=False)
    part_number = Column(String, nullable=False)
    color = Column(String, nullable=False)
    gauge = Column(Float, nullable=False)
    length = Column(Float, nullable=False)
    harness_id = Column(UUID(as_uuid=True), ForeignKey("harnesses.id"), nullable=False)

    harness = relationship("Harness", back_populates="wires")


class Connection(Base):
    __tablename__ = "connections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    harness_id = Column(UUID(as_uuid=True), ForeignKey("harnesses.id"), nullable=False)
    wire_id = Column(UUID(as_uuid=True), ForeignKey("wires.id"), nullable=False)
    from_pin_id = Column(UUID(as_uuid=True), ForeignKey("pins.id"), nullable=False)
    to_pin_id = Column(UUID(as_uuid=True), ForeignKey("pins.id"), nullable=False)

    harness = relationship("Harness", back_populates="connections")
    wire = relationship("Wire")
    from_pin = relationship("Pin", foreign_keys=[from_pin_id])
    to_pin = relationship("Pin", foreign_keys=[to_pin_id])
