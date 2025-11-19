from uuid import UUID

from pydantic import BaseModel, ConfigDict


class NodeData(BaseModel):
    id: str
    label: str
    manufacturer: str | None = None
    part_number: str | None = None
    # Add other component-specific fields as needed


class Node(BaseModel):
    id: str
    type: str
    position: dict[str, float]
    data: NodeData
    width: float | None = None
    height: float | None = None

    model_config = ConfigDict(from_attributes=True)


class EdgeData(BaseModel):
    wire_id: str
    color: str
    # Add other wire-specific fields as needed


class Edge(BaseModel):
    id: str
    source: str
    target: str
    sourceHandle: str | None = None
    targetHandle: str | None = None
    data: EdgeData


class HarnessDesign(BaseModel):
    nodes: list[Node]
    edges: list[Edge]


class DesignData(HarnessDesign):
    pass


class DesignSave(BaseModel):
    design_data: DesignData
    harness_id: UUID


class HarnessDesignSaveResponse(BaseModel):
    status: str
    harness_design_id: int
