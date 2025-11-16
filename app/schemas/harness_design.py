from pydantic import BaseModel


class Node(BaseModel):
    id: str
    position: dict
    data: dict
    type: str


class Edge(BaseModel):
    id: str
    source: str
    target: str


class DesignData(BaseModel):
    nodes: list[Node]
    edges: list[Edge]


class DesignSave(BaseModel):
    design_data: DesignData


class HarnessDesignSaveResponse(BaseModel):
    status: str
    harness_design_id: int
