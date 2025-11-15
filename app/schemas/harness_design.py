from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Node(BaseModel):
    id: str
    type: str
    position: Dict[str, float]
    data: Dict[str, Any]


class Edge(BaseModel):
    id: str
    source: str
    target: str
    sourceHandle: Optional[str] = None
    targetHandle: Optional[str] = None


class DesignData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
