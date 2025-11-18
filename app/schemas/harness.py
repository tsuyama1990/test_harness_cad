from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

# --- Component Schemas for Creation ---


class PinCreate(BaseModel):
    id: str = Field(
        ..., description="Pin identifier within the connector, e.g., '1' or 'A1'"
    )


class ConnectorCreate(BaseModel):
    id: str = Field(
        ...,
        description="User-defined logical identifier for the connector, e.g., 'CONN1'",
    )
    manufacturer: str
    part_number: str
    pins: list[PinCreate]


class WireCreate(BaseModel):
    id: str = Field(
        ..., description="User-defined logical identifier for the wire, e.g., 'W-001'"
    )
    manufacturer: str
    part_number: str
    color: str
    gauge: float
    length: float = Field(..., description="Length of the wire in millimeters")


class ConnectionCreate(BaseModel):
    wire_id: str = Field(
        ..., description="Logical ID of the wire used for the connection"
    )
    from_connector_id: str = Field(
        ..., description="Logical ID of the source connector"
    )
    from_pin_id: str = Field(..., description="Identifier of the source pin")
    to_connector_id: str = Field(
        ..., description="Logical ID of the destination connector"
    )
    to_pin_id: str = Field(..., description="Identifier of the destination pin")
    strip_length_a: float | None = None
    strip_length_b: float | None = None
    terminal_part_number_a: str | None = None
    terminal_part_number_b: str | None = None
    marking_text_a: str | None = None
    marking_text_b: str | None = None


class Connection(ConnectionCreate):
    pass


# --- Harness Schemas ---


class HarnessCreate(BaseModel):
    name: str
    connectors: list[ConnectorCreate]
    wires: list[WireCreate]
    connections: list[ConnectionCreate]


class Harness(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class HarnessFull(HarnessCreate):
    id: UUID
    connections: list[ConnectionCreate]

    model_config = ConfigDict(from_attributes=True)


# --- API Response Schemas ---


class BomItem(BaseModel):
    part_number: str
    manufacturer: str
    quantity: int


class BomResponse(BaseModel):
    connectors: list[BomItem]
    wires: list[BomItem]
    # Terminals can be added later if needed.


class CutlistItem(BaseModel):
    wire_id: str
    part_number: str
    color: str
    length: float


class CutlistResponse(BaseModel):
    items: list[CutlistItem]


class FromToItem(BaseModel):
    wire_id: str
    from_location: str = Field(..., description="e.g., 'CONN1-1'")
    to_location: str = Field(..., description="e.g., 'CONN2-3'")


class FromToResponse(BaseModel):
    items: list[FromToItem]


# --- 3D Schemas ---


class Point3D(BaseModel):
    x: float
    y: float
    z: float


class Path3D(BaseModel):
    points: list[Point3D]


class WireLength(BaseModel):
    length: float


class Wire(WireCreate):
    id: str

    model_config = ConfigDict(from_attributes=True)
