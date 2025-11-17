from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class NodeData(BaseModel):
    id: str
    label: str
    manufacturer: Optional[str] = None
    part_number: Optional[str] = None
    # Add other component-specific fields as needed


class Node(BaseModel):
    id: str
    type: str
    position: dict[str, float]
    data: NodeData
    width: Optional[float] = None
    height: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class EdgeData(BaseModel):
    wire_id: str
    color: str
    # Add other wire-specific fields as needed


class Edge(BaseModel):
    id: str
    source: str
    target: str
    sourceHandle: Optional[str] = None
    targetHandle: Optional[str] = None
    data: EdgeData


class HarnessDesign(BaseModel):
    nodes: List[Node]
    edges: List[Edge]


class DesignData(HarnessDesign):
    pass


class DesignSave(BaseModel):
    design_data: DesignData


class HarnessDesignSaveResponse(BaseModel):
    status: str
    harness_design_id: int
